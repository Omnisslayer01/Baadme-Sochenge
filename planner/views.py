from django.shortcuts import render
from .models import User_state,Vault_Goal,Micro_task

def flashlight_tasks(request, user):
    user_state=User_state.objects.get(user=user)
    user_energy_level=user_state.current_energy_level
    microtask=Micro_task.objects.filter(
        parent_goal__user=user,
        status='vaulted',
        energy_cost__lte=user_energy_level
        )
    flashlighttask=microtask.first()
    return flashlighttask
    




