from django.shortcuts import render
from .models import User_state,Vault_Goal,Micro_task
from django.shortcuts import redirect
def flashlight_tasks(request):
    user=request.user
    user_state=User_state.objects.get(user=user)
    user_energy_level=user_state.current_energy_level
    microtask=Micro_task.objects.filter(
        parent_goal__user=user,
        status='vaulted',
        energy_cost__lte=user_energy_level
        )
    flashlighttask=microtask.first()
    
    if flashlighttask == None:
        taskcost = 0
    else :
        taskcost = flashlighttask.energy_cost

    return render(request, 'planner/index.html',{
        'task':flashlighttask,
        'filtered_tasks':microtask, 
        'task_Cost': taskcost, 
    }
    )

def update_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        action = request.POST.get('action')
        task =  Micro_task.objects.get(id= task_id , parent_goal__user= request.user)
        if action == "complete":
            task.status = "completed"
        elif action == "skip":
            task.skip_count +=1
            if task.skip_count >=3:
                task.status = "intervention"
        task.save()
    return redirect('home')



        


        

        




