from django.contrib import admin
from .models import ProfilJoueur, Transaction, Defi, DefiJoueur


@admin.register(ProfilJoueur)
class ProfilJoueurAdmin(admin.ModelAdmin):
    list_display = ('user', 'niveau', 'xp', 'autocoin_balance', 'created_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('niveau',)
    ordering = ('-xp',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('profil', 'type', 'montant', 'created_at')
    search_fields = ('profil__user__username',)
    list_filter = ('type',)
    ordering = ('-created_at',)


@admin.register(Defi)
class DefiAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type', 'xp_reward', 'ac_reward', 'is_active')
    list_filter = ('type', 'is_active')
    ordering = ('type', 'titre')


@admin.register(DefiJoueur)
class DefiJoueurAdmin(admin.ModelAdmin):
    list_display = ('profil', 'defi', 'progression', 'completed', 'completed_at')
    search_fields = ('profil__user__username', 'defi__titre')
    list_filter = ('completed', 'defi__type')
    ordering = ('-completed_at',)
