from django.contrib import admin
from .models import Message, MessageManager

admin.site.register(Message)
admin.site.register(MessageManager)
