from django.contrib import admin

from .models import *



admin.site.register(Message)

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('pk', 'u1', 'u2')
