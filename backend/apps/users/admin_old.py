from django.contrib import admin
from django.utils.html import format_html
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'country',
        'plan_badge',
        'xp_display',
        'niveau_display',
        'coins_display',
    )
    search_fields = ('user__username', 'user__email')
    list_filter = ('country',)
    ordering = ('-created_at',)

    def plan_badge(self, obj):
        plan = getattr(obj, 'plan', 'free')
        css_map = {
            'pro': 'ai-badge-violet',
            'business': 'ai-badge-amber',
            'free': 'ai-badge-gray',
        }
        css = css_map.get(plan, 'ai-badge-gray')
        return format_html('<span class="ai-badge {}">{}</span>', css, str(plan).upper())

    plan_badge.short_description = 'Plan'

    def coins_display(self, obj):
        return format_html('<span style="color:#F59E0B;font-weight:600">🪙 {}</span>', obj.coins)

    coins_display.short_description = 'Coins'

    def xp_display(self, obj):
        return format_html('<span style="color:#6C63FF">⚡ {} XP</span>', obj.xp)

    xp_display.short_description = 'XP'

    def niveau_display(self, obj):
        return format_html('<span class="ai-badge ai-badge-violet">Niv. {}</span>', obj.level)

    niveau_display.short_description = 'Niveau'
