from django.contrib import admin
from .models import Chat

class ChatAdmin(admin.ModelAdmin):
    filter_horizontal = ('participants',)

admin.site.register(Chat, ChatAdmin)
