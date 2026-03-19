from django.db import models
from django.contrib.auth.models import User

class User_state(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_energy_level=models.IntegerField()
    last_assessed=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} has {self.current_energy_level} and was last assessed at {self.last_assessed}'

class Vault_Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} is active= {self.is_active} and was created at {self.created_at}'

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

    def __str__(self):
        return f'{self.title} has {self.energy_cost} and has status= {self.status} having deadline {self.soft_deadline}'



    

