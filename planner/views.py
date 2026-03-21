    from django.shortcuts import render
    from .models import User_state,Vault_Goal,Micro_task

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

    def CompleteIt(request):
        user = request.user
        microtask= Micro_task.objects.filter(
            parent_goal__user = user,
            status = ""
            )
        if status == 0:
            microtask.skip_count +=1
            if microtask.skip_count > 2:
                microtask.status = "Intervention"
        elif statuss ==1:
            microtask.status = "Completed"
            flashlighttask.pop

        


        

        




