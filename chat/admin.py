# Register your models here.
from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver','message', 'timestamp')

admin.site.register(Message,MessageAdmin)