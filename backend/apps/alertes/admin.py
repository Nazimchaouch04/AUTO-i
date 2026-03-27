from django.contrib import admin
from .models import Alerte


@admin.register(Alerte)
class AlerteAdmin(admin.ModelAdmin):
    list_display = ('titre', 'user', 'email_actif', 'est_active', 'created_at', 'last_triggered')
    search_fields = ('titre', 'user__username')
    list_filter = ('email_actif', 'est_active', 'pays')
    ordering = ('-created_at',)
