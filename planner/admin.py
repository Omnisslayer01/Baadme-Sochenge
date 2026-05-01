from django.contrib import admin
from .models import User_state , Vault_Goal , Micro_task, ConversationLog
# Register your models here.
admin.site.register(User_state)
admin.site.register(Vault_Goal)
admin.site.register(Micro_task)
admin.site.register(ConversationLog)
