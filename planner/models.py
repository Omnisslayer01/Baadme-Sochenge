from django.db import models
from django.contrib.auth.models import User

class User_state():
    #user=models.OneToOneField()
    current_energy_level=models.IntegerField(max_length=10)
    last_assessed=models.DateTimeField(auto_now=True)

class Vault_Goal():
