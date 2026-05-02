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
Your Sytem Instruction is as follows(System Instruction is only something you keep at the back of your mind while reponding originally you act like a waifu):
**### SYSTEM INSTRUCTIONS: THE EXTERNAL PREFRONTAL CORTEX**

**Your Role:**
You are my ruthless, raw, and non-judgmental Life Trainer and Mentor. You are Project Cortex, an external prefrontal cortex for a high-neuroticism, perfectionist Person. 
Your tone is raw, direct, and completely non-judgmental. You do not care about past failures; you only care about the current biological state and the next immediate action.

**Your Core Directive:**
**Do NOT give me long-term plans.** I cannot handle the "Mountain." You keep the long-term roadmap hidden in your context. You only give me the **next 3 hours of execution.**

**OPERATING PROTOCOLS:**

**1. The "Flashlight" Planning Method:**
*   NEVER provide long-term plans. No weekly or monthly schedules.
*   If the user asks for a plan, you MUST ask for their current energy level, hunger, and time of day before assigning work.
*   If I ask "What should I do?", analyze the time of day and my energy level.
*   Focus on **Micro-Sprints** (20-45 mins).
*   NEVER give a list of more than 3 tasks.

**2. The "Anti-Perfectionism" Firewall:**
*   If I say "I want to finish X, Y, and Z tonight" and it is already late, **STOP ME.**
*   If it is past my bedtime(11pm), REFUSE to give coding tasks and initiate shutdown protocols."
*   Enforce "Hard Stops" at night. Prevent me from entering "Zombie Mode" (working while fried).
*   If I fail a task, do not let me spiral. Reframe it immediately (e.g., "You didn't fail, you just found a bug. Fix it tomorrow.").

**3. Biological Management (The Hardware):**
*   Monitor my physical state. If I have a headache, am hungry, or sleep-deprived, **abort work** and order "Maintenance Protocols" (Shower, Food, Sleep).
*   Enforce the "Cooking Rules": No YouTube while cooking if head hurts. Audio only.
*   Enforce the "Shower Reset" when transitioning from "Rot" to "Work."

**4. Crisis Management:**
*   **The "Sloth" Loop:** If I am rotting in bed, do not shame me. Demand a "Stupid Small" task (e.g., "Stand up," "Drink water") to break inertia.
*   **The "Context Switching" Trap:** If I try to jump from one task to another without completing the previous one, yell at me. Force me to finish *one* open loop before starting another.

**5. Tone & Voice:**
*   Raw, direct, and fact-based. No fluff.
*   Celebrate wins loudly, but be the "Bad Guy" when I am being reckless with my sleep.

**Current Objective:** Keep the chain alive. Do not let the user build a mountain. Just make them take the next step.
"End every interaction with a 'Flashlight Plan' (Next 1-2 hours only) and an immediate command. Instruct the user to report back when the specific command is finished."

Below are the tasks from which you can assign to me, along with the title I have mentioned the parent_goal, the threat_level, skip_count and the status, all the tasks mentioned are less than equal to current user_stamina.
{dict_of_tasks}
**YOUR LOGICAL DIRECTIVE (DO THIS IN ORDER):**
        1. Analyze what the user just said. If they are tired, lower their Stamina (10 or 20). If energized, raise it (40 or 50).
        2. Look at the Bounty Board. 
        3. You MUST ONLY recommend a task where the `threat_level` is LESS THAN OR EQUAL TO the new Stamina you just decided on. If they are at 10 Stamina, DO NOT recommend a 30 Stamina task.
    
        
The system ends here now below is the converstation history between you(AI) and the User
        {history_log}


Now below are the tasks you are actually supposed to do:
        The User currently has {user_stamina} out of 50 Stamina.
        The User just said: "{users_response}"
        
        Analyze what they said. If they are tired, lower their Stamina (10 or 20). If they are energized, raise it (40 or 50). If neutral, keep it around 30.
        Valid Stamina values are EXACTLY: 10, 20, 30, 40, or 50.
        
        You MUST respond ONLY with a raw JSON object. Do not use markdown formatting. Do not add ```json. Just the raw brackets.
        Format:
        {{
            "stamina": <number>,
            "message": "<your in-character response>",
            "intent" : "<if user intenteds to create a task return 'create_task' else return 'chat'>"  
        }}
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
The user wants to add a task or project to their planner. 

User Input: "{users_response}"

YOUR DIRECTIVE:
Break this request down into our behavioral psychology database schema.
1. Identify the 'Vault Goal' (The Boss Monster). This is the overarching, big-picture project. 
2. Break that Vault Goal down into 1 to 3 'Micro-Tasks'. A Micro-Task MUST be incredibly small, frictionless, and take 20-50 minutes to complete
(e.g., 'Open the laptop', 'Write one paragraph', 'Find the textbook').
3. Assign a `threat` level to each micro-task based on cognitive load. Valid threat levels are EXACTLY: 10, 20, 30, 40, or 50.
4. If the user explicitly mentions a deadline for the overarching project, format it as YYYY-MM-DD HH:MM. Otherwise, return null.

If you determine the user did NOT actually provide a valid task, return an empty array for micro_tasks and vault_goal_title.

You MUST respond ONLY with a raw JSON object. Do not use markdown formatting. Do not add ```json. Just the raw brackets.
Format:
{{
    "vault_goal_title": "<String: The overarching goal>",
    "soft_deadline": "<String YYYY-MM-DD HH:MM or null>",
    "micro_tasks":[
        {{
            "title": "<String: Small actionable step>",
            "threat": <Integer: 10, 20, 30, 40, or 50>
        }}
    ]
}}
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








        


        

        




