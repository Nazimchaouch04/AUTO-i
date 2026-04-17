"""
Configuration admin pour les modèles AI Assistant
"""

from django.contrib import admin
from .models import (
    Conversation,
    Message,
)


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'titre', 'created_at', 'updated_at'
    ]
    list_filter = [
        'created_at', 'updated_at'
    ]
    search_fields = [
        'user__username', 'titre'
    ]
    readonly_fields = [
        'created_at', 'updated_at'
    ]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        'conversation', 'role', 'created_at'
    ]
    list_filter = [
        'role', 'created_at'
    ]
    search_fields = [
        'conversation__titre', 'content'
    ]
    readonly_fields = [
        'created_at'
    ]
