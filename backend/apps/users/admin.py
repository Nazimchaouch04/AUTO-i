from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from django.utils.html import format_html
from .models import UserProfile
from .profiles_admin import UserProfileAdmin


# Unregister the default User admin to register our enhanced version
admin.site.unregister(User)


# Inline pour afficher le profil dans l'admin User
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profil utilisateur'
    fields = (
        'country',
        'xp_display',
        'level_display',
        'coins_display',
        'plan_badge',
    )
    readonly_fields = ('xp_display', 'level_display', 'coins_display', 'plan_badge')
    
    def xp_display(self, obj):
        return format_html('<span style="color:#6C63FF">⚡ {} XP</span>', obj.xp)
    xp_display.short_description = 'XP'
    
    def level_display(self, obj):
        return format_html('<span class="ai-badge ai-badge-violet">Niv. {}</span>', obj.level)
    level_display.short_description = 'Niveau'
    
    def coins_display(self, obj):
        return format_html('<span style="color:#F59E0B;font-weight:600">🪙 {}</span>', obj.coins)
    coins_display.short_description = 'Coins'
    
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


# Enhanced User Admin
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'username_display',
        'email_display',
        'first_name_display',
        'last_name_display',
        'staff_display',
        'active_display',
        'date_joined_display',
        'profile_info'
    )
    list_filter = (
        'is_staff', 'is_superuser', 'is_active', 
        'date_joined', 'last_login'
    )
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    inlines = [UserProfileInline]
    
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('username', 'password', ('first_name', 'last_name'), 'email'),
            'classes': ('wide',),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('wide',),
        }),
        ('Dates importantes', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',),
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    
    def username_display(self, obj):
        return format_html('<strong style="color:#F0F0F5">{}</strong>', obj.username)
    username_display.short_description = 'Nom d\'utilisateur'
    
    def email_display(self, obj):
        return format_html('<span style="color:#8B8BA0">{}</span>', obj.email)
    email_display.short_description = 'Email'
    
    def first_name_display(self, obj):
        return format_html('<span style="color:#F0F0F5">{}</span>', obj.first_name)
    first_name_display.short_description = 'Prénom'
    
    def last_name_display(self, obj):
        return format_html('<span style="color:#F0F0F5">{}</span>', obj.last_name)
    last_name_display.short_description = 'Nom'
    
    def staff_display(self, obj):
        if obj.is_superuser:
            return format_html('<span class="ai-badge ai-badge-red">👑 Superadmin</span>')
        elif obj.is_staff:
            return format_html('<span class="ai-badge ai-badge-amber">👤 Staff</span>')
        return format_html('<span class="ai-badge ai-badge-gray">👤 Utilisateur</span>')
    staff_display.short_description = 'Rôle'
    
    def active_display(self, obj):
        if obj.is_active:
            return format_html('<span class="ai-badge ai-badge-green">● Actif</span>')
        return format_html('<span class="ai-badge ai-badge-gray">● Inactif</span>')
    active_display.short_description = 'Statut'
    
    def date_joined_display(self, obj):
        return format_html('<span style="color:#8B8BA0">{}</span>', obj.date_joined.strftime('%d/%m/%Y'))
    date_joined_display.short_description = 'Inscription'
    
    def profile_info(self, obj):
        try:
            profile = obj.profile
            plan = getattr(profile, 'plan', 'free')
            return format_html(
                '<span class="ai-badge ai-badge-violet">Niv.{}</span> '
                '<span style="color:#F59E0B">🪙{}</span> '
                '<span class="ai-badge ai-badge-amber">{}</span>',
                profile.level, profile.coins, plan.upper()
            )
        except:
            return format_html('<span class="ai-badge ai-badge-gray">Pas de profil</span>')
    profile_info.short_description = 'Profil'


# Unregister the default Group admin to register our enhanced version
admin.site.unregister(Group)


# Enhanced Group Admin
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name_display', 'user_count', 'permissions_display')
    search_fields = ('name',)
    ordering = ('name',)
    filter_horizontal = ('permissions',)
    
    fieldsets = (
        ('Informations du groupe', {
            'fields': ('name', 'permissions'),
            'classes': ('wide',),
        }),
    )
    
    def name_display(self, obj):
        return format_html('<strong style="color:#F0F0F5">{}</strong>', obj.name)
    name_display.short_description = 'Nom du groupe'
    
    def user_count(self, obj):
        count = obj.user_set.count()
        return format_html('<span class="ai-badge ai-badge-violet">{}</span>', count)
    user_count.short_description = 'Utilisateurs'
    
    def permissions_display(self, obj):
        count = obj.permissions.count()
        if count == 0:
            return format_html('<span class="ai-badge ai-badge-gray">Aucune</span>')
        elif count < 10:
            return format_html('<span class="ai-badge ai-badge-green">{}</span>', count)
        else:
            return format_html('<span class="ai-badge ai-badge-amber">{}</span>', count)
    permissions_display.short_description = 'Permissions'


# Enhanced UserProfile Admin (déjà importé depuis profiles_admin.py)
# UserProfileAdmin est déjà enregistré via l'import
