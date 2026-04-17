"""
Configuration admin pour les modèles Notifications
"""

from django.contrib import admin
from .models import (
    CanalNotification,
)


@admin.register(CanalNotification)
class CanalNotificationAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'canal', 'valeur', 'is_verified', 'is_active', 'created_at'
    ]
    list_filter = [
        'canal', 'is_verified', 'is_active', 'created_at'
    ]
    search_fields = [
        'user__username', 'valeur'
    ]
    readonly_fields = [
        'created_at', 'updated_at'
    ]
