from django.shortcuts import render
from .models import User_state,Vault_Goal,Micro_task
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import os
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))


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
    if request.method == 'POST':
        users_response = request.POST.get('user_response') 
        
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        prompt = f"""
        Act as a cheerful, empathetic Anime Guild Receptionist. 
        The Guild Master (Hero) just said: "{users_response}"
        Respond in character in 2 short sentences. Be encouraging!
        """
        response = model.generate_content(prompt)
        ai_reply = response.text
    
        request.session['waifu_message'] = ai_reply
        
        return redirect('home')
    return render(request, 'planner/voice.html')








        


        

        




