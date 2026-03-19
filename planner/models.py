from django.db import models
from django.contrib.auth.models import User

class User_state(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    current_energy_level=models.IntegerField()
    last_assessed=models.DateTimeField(auto_now=True)

class Vault_Goal(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Micro_task(models.Model):
    parent_goal = models.ForeignKey(Vault_Goal , on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    energy_cost = models.IntegerField()
    skip_count = models.IntegerField(default=0)
    STATUS_CHOICES =[
    ('vaulted', 'Vaulted'),
    ('flashlight', 'Flashlight'),
    ('completed', 'Completed'),
    ('intervention', 'Intervention')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='vaulted')
    soft_deadline = models.DateTimeField(null=True , blank= True)



    

