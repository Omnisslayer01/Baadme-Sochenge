from django.db import models
from django.contrib.auth.models import User


class ThreatLevel(models.IntegerChoices):
    D_Rank_Mission=10,'D-Rank'
    C_Rank_Mission=20,'C-Rank'
    B_Rank_Mission=30,'B-Rank'
    A_Rank_Mission=40,'A-Rank'
    S_Rank_Mission=50,'S-Rank'


class User_state(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_stamina=models.IntegerField(choices=ThreatLevel.choices, default=ThreatLevel.C_Rank_Mission )
    last_assessed=models.DateTimeField(auto_now=True )

    def __str__(self):
        return f'{self.user} {self.last_assessed} is ready to do {self.get_current_stamina_display()} Missions.'

class Vault_Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} created {self.title} {self.created_at} is_active={self.is_active}'

class Micro_task(models.Model):
    parent_goal = models.ForeignKey(Vault_Goal , on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    threat = models.IntegerField(choices=ThreatLevel.choices)
    skip_count = models.IntegerField(default=0)
    STATUS_CHOICES =[
    ('bounty_board', 'Bounty_Board'),
    ('active_hunt','Active_hunt'),
    ('tactical_retreat', 'Tactical_Retreat'),
    ('defeated', 'Defeated'),
    ('intervention','Intervention')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='bounty_board')
    soft_deadline = models.DateTimeField(null=True , blank= True)

    def __str__(self):
        return f'{self.title} is a {self.get_threat_display()} Mission and has status={self.status} having deadline {self.soft_deadline}'



    

