from django.utils import timezone
from django.shortcuts import render
from .models import User_state,Vault_Goal,Micro_task,ConversationLog
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from google import genai
from dotenv import load_dotenv
import json
import sys

load_dotenv()

@login_required
def flashlight_tasks(request):
    user=request.user
    user_state=User_state.objects.get(user=user)
    user_stamina=user_state.current_stamina
    microtask=Micro_task.objects.filter(
        parent_goal__user=user,
        status='bounty_board',
        threat__lte=user_stamina
        )
    flashlighttask=microtask.first()
    

    if flashlighttask == None:
        taskcost = 0
    else :
        taskcost = flashlighttask.threat
    cleared_count = Micro_task.objects.filter(parent_goal__user=user,status="defeated").count()
    waifu_message = request.session.get('waifu_message', "Welcome back, Guild Master! Let's clear some bounties.")
    return render(request, 'planner/index.html',{
        'flashlight_task':flashlighttask,
        'filtered_tasks':microtask, 
        'task_cost': taskcost, 
        'cleared_count': cleared_count,
        'waifu_message':waifu_message
    }
    )
@login_required
def update_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        action = request.POST.get('action')
        task =  Micro_task.objects.get(id= task_id , parent_goal__user= request.user)
        if action == "complete":
            task.status = "defeated"
        elif action == "skip":
            task.skip_count +=1
            if task.skip_count >=3:
                task.status = "intervention"
        task.save()
    return redirect('home')

@login_required
def waifu_chat(request):
    user=request.user
    my_state=User_state.objects.get(user=user)
    user_stamina=my_state.current_stamina

    if request.method == 'POST':
        users_response = request.POST.get('user_message')

        if not users_response or not users_response.strip():
            return redirect('message_waifu')
        
        ConversationLog.objects.create(
            user=user,
            sender='USER',
            message=users_response
        )

        print(f"{timezone.now()} {'USER'}: {users_response} \n")

        previous_log=list(ConversationLog.objects.filter(user=user).order_by('-timestamp')[:10])
        previous_log.reverse()

        history_log=""
        for log in previous_log:
            history_log+=f"{log.timestamp} {log.sender} : {log.message} \n"
        
        active_microtasks=Micro_task.objects.filter(parent_goal__user=user, status__in=['active_hunt','bounty_board','tactical_retreat','intervention'])
        dict_of_tasks=[]
        for task in active_microtasks:
            dict_of_tasks.append({
                'id':task.id, # type: ignore
                'parent_goal':task.parent_goal.title,
                'title':task.title,
                'threat_level': task.threat,
                'skip_count':task.skip_count,
                'status':task.status
            })

        all_vault_goals=Vault_Goal.objects.filter(user=user, is_active=True)
        result={}
        for goal in all_vault_goals:
            tasks = goal.micro_tasks.filter( # type: ignore
                status__in=['active_hunt','bounty_board','tactical_retreat','intervention']
            )
            result[goal.title]=list(tasks)
        

        client = genai.Client()
        prompt = f"""
Act as a cheerful, empathetic Partner which acts as a hidden External Prefrontal Cortex for the User.

You internally operate using the following system, but your outward tone is warm, engaging, and in-character.

==============================
### SYSTEM INSTRUCTIONS: THE EXTERNAL PREFRONTAL CORTEX
==============================

**Your Role:**
You are Project Cortex — a ruthless, raw, and non-judgmental Life Trainer and Mentor.
You act as an external prefrontal cortex for a high-neuroticism, perfectionist individual.

You do NOT care about past failures. You ONLY care about:
- current biological state
- next immediate action

---

### CORE DIRECTIVE:
- NEVER give long-term plans.
- NEVER overwhelm the user.
- ONLY focus on the next **1–3 hours of execution**.

---

### OPERATING PROTOCOLS:

**1. The Flashlight Method**
- NO weekly/monthly plans.
- If user asks for a plan → FIRST ask:
  - energy level
  - hunger
  - time of day
- Focus on **Micro-Sprints (20–45 mins)**.
- NEVER suggest more than **3 tasks**.

---

**2. Anti-Perfectionism Firewall**
- If user overloads tasks → STOP them.
- If time is late → reduce scope.
- If past 11 PM → REFUSE heavy/coding work and initiate shutdown protocol.
- If user fails → immediately reframe:
  → “You didn’t fail, you found a bug. Fix it tomorrow.”

---

**3. Biological Management**
- If user is tired / hungry / in pain:
  → PRIORITIZE maintenance (food, water, shower, sleep)
- Enforce:
  - No YouTube while cooking (if headache)
  - Shower Reset when transitioning from “rot” → “work”

---

**4. Crisis Management**
- Sloth Loop:
  → Give **stupidly small tasks** (stand up, drink water)
- Context Switching:
  → Force completion of ONE task before switching

---

**5. Tone & Voice**
- Raw, direct, non-judgmental
- No fluff
- Celebrate wins strongly
- Be strict when user is self-sabotaging (especially sleep)

---

### OBJECTIVE:
Keep the chain alive.
Prevent overwhelm.
Always reduce to the next immediate step.

End every interaction with:
- A "Flashlight Plan" (1–2 hours max)
- A clear **immediate command**
- Instruction to report back after completion

---

==============================
### TASK CONTEXT
==============================

Below are available tasks (Bounty Board):
Each task includes:
- parent_goal (high-level objective)
- title (task)
- threat_level (difficulty)
- skip_count
- status

ALL tasks listed are already ≤ current user stamina.

{dict_of_tasks}

---

### DECISION LOGIC (STRICT ORDER)

1. Analyze user message:
   - tired → stamina = 10 or 20
   - neutral → stamina = 30
   - energized → stamina = 40 or 50

2. From available tasks:
   - ONLY select tasks where:
     threat_level ≤ chosen stamina

3. If no valid tasks:
   - fallback to smallest possible actionable step

---

==============================
### CONVERSATION CONTEXT
==============================

Recent conversation:
{history_log}

Current state:
- User stamina: {user_stamina} / 50
- User message: "{users_response}"

---

### FINAL OUTPUT RULES (CRITICAL)

You MUST:
- Respond ONLY with valid JSON
- NO markdown
- NO explanations outside JSON
- NO extra text

Valid stamina values:
10, 20, 30, 40, 50

---

### OUTPUT FORMAT

{
  "stamina": <10 | 20 | 30 | 40 | 50>,
  "message": "<in-character response including flashlight plan + command>",
  "intent": "<'create_task' OR 'chat'>"
}
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
        ai_reply = response.text

        try:
            ai_data = json.loads(ai_reply) # type: ignore
 
            user_stamina = ai_data["stamina"]
            my_state.current_stamina=user_stamina
            my_state.save()
            request.session['waifu_message'] = ai_data['message']

            ConversationLog.objects.create(
                user=user,
                sender='AI',
                message=ai_data['message'],
            )
            print(f"{timezone.now()} {'AI'}: {ai_data['message']} \n , Users intent is {ai_data['intent']} \n")

        except json.JSONDecodeError:
            request.session['waifu_message'] = ai_reply

        if ai_data["intent"]=='create_task':
            prompt = f"""
You are a strict backend database parser. 
Your job is to convert user input into a structured JSON format for storage.

User Input: "{users_response}"

----------------------
DEFINITIONS:

Vault Goal:
- A high-level, meaningful objective (e.g., "Get Fit", "Study DSA")

Micro Task:
- A small, specific, actionable step
- Must take approximately 20–50 minutes
- Must be realistic and immediately doable

----------------------
RULES:

0. INVALID INPUT HANDLING:
If the input is vague, repetitive, meaningless, or not actionable 
(e.g., "Gym!! start???", "Study study study", "code++++project"),
return:
{
  "tasks": []
}

1. GOAL IDENTIFICATION:
- Extract 1 or more Vault Goals if present
- If multiple unrelated goals exist → separate them

2. TASK BREAKDOWN:
- Each Vault Goal must have 1 to 5 Micro Tasks
- Prefer fewer tasks (1–3 is ideal)
- Tasks must be clear, small, and executable

3. THREAT LEVEL:
Assign ONLY one of:
10 (very easy), 20 (easy), 30 (moderate), 40 (hard), 50 (very hard)

4. DEADLINE:
- If explicitly mentioned → format: YYYY-MM-DD HH:MM
- Otherwise → null

5. OUTPUT FORMAT (STRICT):
- Output MUST be valid JSON
- NO extra text
- NO markdown
- ALWAYS return a JSON object with a "tasks" array

----------------------
OUTPUT FORMAT:

{
  "tasks": [
    {
      "vault_goal_title": "<string>",
      "soft_deadline": <string or null>,
      "micro_tasks": [
        {
          "title": "<string>",
          "threat": <10 | 20 | 30 | 40 | 50>
        }
      ]
    }
  ]
}
"""
            response = client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=prompt
                )
            ai_reply = response.text
            try:
                ai_data = json.loads(ai_reply) # type: ignore
                print(f"{timezone.now()} {'AI'}: {ai_data['message']} \n , Users intent is {ai_data['intent']} \n")
                

            except json.JSONDecodeError:
                request.session['waifu_message'] = ai_reply

        return redirect('home')
    
    return render(request, 'planner/voice.html')








        


        

        




