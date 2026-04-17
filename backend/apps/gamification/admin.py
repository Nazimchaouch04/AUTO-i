from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, Count
from .models import ProfilJoueur, Transaction, Defi, DefiJoueur, BoutiqueItem, AchatJoueur


@admin.register(ProfilJoueur)
class ProfilJoueurAdmin(admin.ModelAdmin):
    list_display = (
        'user_display',
        'level_display',
        'xp_display',
        'progression_display',
        'coins_display',
        'estimations_display',
        'created_at'
    )
    search_fields = ('user__username', 'user__email')
    list_filter = ('niveau', 'created_at')
    ordering = ('-xp', '-niveau')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',),
            'classes': ('wide',),
        }),
        ('Niveau et expérience', {
            'fields': (('niveau', 'xp'), 'estimations_ce_mois'),
            'classes': ('wide',),
        }),
        ('Monnaie virtuelle', {
            'fields': ('autocoin_balance',),
            'classes': ('wide',),
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    # Actions personnalisées
    actions = ['ajouter_xp', 'ajouter_coins', 'reset_niveau']
    
    def user_display(self, obj):
        return format_html('<span class="ai-badge ai-badge-violet">{}</span>', obj.user.username)
    user_display.short_description = 'Utilisateur'
    
    def level_display(self, obj):
        colors = {
            1: 'ai-badge-gray',
            2: 'ai-badge-green', 
            3: 'ai-badge-teal',
            4: 'ai-badge-amber',
            5: 'ai-badge-red',
            6: 'ai-badge-violet',
        }
        css = colors.get(obj.niveau, 'ai-badge-gray')
        return format_html(
            '<span class="ai-badge {}">Niv {}</span><br>'
            '<span style="color:#8B8BA0;font-size:11px">{}</span>',
            css, obj.niveau, obj.nom_niveau()
        )
    level_display.short_description = 'Niveau'
    
    def xp_display(self, obj):
        return format_html(
            '<span style="color:#6C63FF;font-weight:600">⚡ {} XP</span>',
            obj.xp
        )
    xp_display.short_description = 'XP'
    
    def progression_display(self, obj):
        if obj.niveau >= 6:
            return format_html('<span class="ai-badge ai-badge-violet">MAX</span>')
        
        xp_prochain = obj.xp_prochain_niveau()
        progression = obj.progression_pct()
        
        return format_html(
            '<div style="width:100px; background:#333; border-radius:10px; overflow:hidden;">'
            '<div style="width:{}%; background:linear-gradient(90deg, #6C63FF, #00D4AA); height:8px;"></div>'
            '</div>'
            '<span style="color:#8B8BA0;font-size:11px">{}/{} XP</span>',
            progression, obj.xp, xp_prochain
        )
    progression_display.short_description = 'Progression'
    
    def coins_display(self, obj):
        return format_html(
            '<span style="color:#F59E0B;font-weight:600">🪙 {} AC</span>',
            obj.autocoin_balance
        )
    coins_display.short_description = 'AutoCoins'
    
    def estimations_display(self, obj):
        if obj.estimations_ce_mois == 0:
            return format_html('<span style="color:#55556A">0</span>')
        elif obj.estimations_ce_mois < 5:
            return format_html('<span class="ai-badge ai-badge-green">{}</span>', obj.estimations_ce_mois)
        else:
            return format_html('<span class="ai-badge ai-badge-amber">{}</span>', obj.estimations_ce_mois)
    estimations_display.short_description = 'Estimations/mois'
    
    def ajouter_xp(self, request, queryset):
        # Action simulée pour démonstration
        count = queryset.count()
        self.message_user(
            request, 
            f'{count} joueurs sélectionnés pour ajout XP (simulation). '
            'Fonctionnalité à implémenter avec formulaire de saisie.'
        )
    ajouter_xp.short_description = 'Ajouter XP (simulation)'
    
    def ajouter_coins(self, request, queryset):
        # Action simulée pour démonstration
        count = queryset.count()
        self.message_user(
            request, 
            f'{count} joueurs sélectionnés pour ajout AutoCoins (simulation). '
            'Fonctionnalité à implémenter avec formulaire de saisie.'
        )
    ajouter_coins.short_description = 'Ajouter AutoCoins (simulation)'
    
    def reset_niveau(self, request, queryset):
        updated = queryset.update(niveau=1, xp=0)
        self.message_user(request, f'{updated} joueurs réinitialisés au niveau 1.')
    reset_niveau.short_description = 'Réinitialiser au niveau 1'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'profil_display',
        'type_display',
        'amount_display',
        'description_display',
        'created_at'
    )
    search_fields = ('profil__user__username', 'description')
    list_filter = ('type', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Transaction', {
            'fields': ('profil', 'type', 'montant', 'description'),
            'classes': ('wide',),
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    
    def profil_display(self, obj):
        return format_html('<span class="ai-badge ai-badge-violet">{}</span>', obj.profil.user.username)
    profil_display.short_description = 'Joueur'
    
    def type_display(self, obj):
        colors = {
            'gain_estimation': 'ai-badge-teal',
            'gain_bonne_affaire': 'ai-badge-green',
            'gain_defi': 'ai-badge-amber',
            'depense_boutique': 'ai-badge-red',
            'gain_battle': 'ai-badge-violet',
        }
        css = colors.get(obj.type, 'ai-badge-gray')
        return format_html('<span class="ai-badge {}">{}</span>', css, obj.get_type_display())
    type_display.short_description = 'Type'
    
    def amount_display(self, obj):
        if obj.montant > 0:
            return format_html('<span style="color:#00D4AA;font-weight:600">+{}</span>', obj.montant)
        else:
            return format_html('<span style="color:#F59E0B;font-weight:600">{}</span>', obj.montant)
    amount_display.short_description = 'Montant'
    
    def description_display(self, obj):
        return format_html('<span style="color:#8B8BA0">{}</span>', obj.description[:50] + '...' if len(obj.description) > 50 else obj.description)
    description_display.short_description = 'Description'


@admin.register(Defi)
class DefiAdmin(admin.ModelAdmin):
    list_display = (
        'titre_display',
        'type_display',
        'rewards_display',
        'target_display',
        'status_display'
    )
    search_fields = ('titre', 'description')
    list_filter = ('type', 'is_active')
    ordering = ('type', 'titre')
    
    fieldsets = (
        ('Défi', {
            'fields': ('titre', 'description', 'type'),
            'classes': ('wide',),
        }),
        ('Récompenses', {
            'fields': (('xp_reward', 'ac_reward'),),
            'classes': ('wide',),
        }),
        ('Paramètres', {
            'fields': ('cible_count', 'is_active'),
            'classes': ('wide',),
        }),
    )
    
    def titre_display(self, obj):
        return format_html('<strong style="color:#F0F0F5">{}</strong>', obj.titre[:40] + '...' if len(obj.titre) > 40 else obj.titre)
    titre_display.short_description = 'Titre'
    
    def type_display(self, obj):
        colors = {
            'quotidien': 'ai-badge-green',
            'hebdomadaire': 'ai-badge-amber',
            'mensuel': 'ai-badge-red',
            'legendaire': 'ai-badge-violet',
        }
        css = colors.get(obj.type, 'ai-badge-gray')
        return format_html('<span class="ai-badge {}">{}</span>', css, obj.get_type_display())
    type_display.short_description = 'Type'
    
    def rewards_display(self, obj):
        return format_html(
            '<span style="color:#6C63FF">⚡{}</span> | '
            '<span style="color:#F59E0B">🪙{}</span>',
            obj.xp_reward, obj.ac_reward
        )
    rewards_display.short_description = 'Récompenses'
    
    def target_display(self, obj):
        return format_html('<span class="ai-badge ai-badge-teal">{}</span>', obj.cible_count)
    target_display.short_description = 'Cible'
    
    def status_display(self, obj):
        if obj.is_active:
            return format_html('<span class="ai-badge ai-badge-green">● Actif</span>')
        return format_html('<span class="ai-badge ai-badge-gray">● Inactif</span>')
    status_display.short_description = 'Statut'


@admin.register(DefiJoueur)
class DefiJoueurAdmin(admin.ModelAdmin):
    list_display = (
        'player_display',
        'defi_display',
        'progression_display',
        'status_display',
        'completed_at_display'
    )
    search_fields = ('profil__user__username', 'defi__titre')
    list_filter = ('completed', 'defi__type')
    ordering = ('-completed_at',)
    readonly_fields = ('completed_at',)
    
    fieldsets = (
        ('Participation', {
            'fields': ('profil', 'defi'),
            'classes': ('wide',),
        }),
        ('Progression', {
            'fields': (('progression', 'completed'), 'completed_at'),
            'classes': ('wide',),
        }),
    )
    
    def player_display(self, obj):
        return format_html('<span class="ai-badge ai-badge-violet">{}</span>', obj.profil.user.username)
    player_display.short_description = 'Joueur'
    
    def defi_display(self, obj):
        return format_html('<strong style="color:#F0F0F5">{}</strong>', obj.defi.titre[:30] + '...' if len(obj.defi.titre) > 30 else obj.defi.titre)
    defi_display.short_description = 'Défi'
    
    def progression_display(self, obj):
        if obj.completed:
            return format_html('<span class="ai-badge ai-badge-teal">✓ Terminé</span>')
        
        pct = min(100, (obj.progression / obj.defi.cible_count) * 100) if obj.defi.cible_count > 0 else 0
        return format_html(
            '<div style="width:100px; background:#333; border-radius:10px; overflow:hidden;">'
            '<div style="width:{}%; background:linear-gradient(90deg, #F59E0B, #00D4AA); height:8px;"></div>'
            '</div>'
            '<span style="color:#8B8BA0;font-size:11px">{}/{} ({:.0f}%)</span>',
            pct, obj.progression, obj.defi.cible_count, pct
        )
    progression_display.short_description = 'Progression'
    
    def status_display(self, obj):
        if obj.completed:
            return format_html('<span class="ai-badge ai-badge-teal">✓ Complété</span>')
        return format_html('<span class="ai-badge ai-badge-amber">⏳ En cours</span>')
    status_display.short_description = 'Statut'
    
    def completed_at_display(self, obj):
        if obj.completed_at:
            return format_html('<span style="color:#8B8BA0">{}</span>', obj.completed_at.strftime('%d/%m %H:%M'))
        return format_html('<span style="color:#55556A">—</span>')
    completed_at_display.short_description = 'Terminé le'


@admin.register(BoutiqueItem)
class BoutiqueItemAdmin(admin.ModelAdmin):
    list_display = (
        'nom_display',
        'price_display',
        'created_at'
    )
    search_fields = ('nom', 'description')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Article boutique', {
            'fields': ('nom', 'description', 'prix_ac', 'image_url', 'slug'),
            'classes': ('wide',),
        }),
    )
    
    def nom_display(self, obj):
        return format_html('<strong style="color:#F0F0F5">{}</strong>', obj.nom)
    nom_display.short_description = 'Article'
    
    def price_display(self, obj):
        return format_html('<span style="color:#F59E0B;font-weight:600">🪙 {} AC</span>', obj.prix_ac)
    price_display.short_description = 'Prix'


@admin.register(AchatJoueur)
class AchatJoueurAdmin(admin.ModelAdmin):
    list_display = (
        'player_display',
        'item_display',
        'date_display'
    )
    search_fields = ('profil__user__username', 'item__nom')
    ordering = ('-date_achat',)
    readonly_fields = ('date_achat',)
    
    fieldsets = (
        ('Achat', {
            'fields': ('profil', 'item'),
            'classes': ('wide',),
        }),
        ('Métadonnées', {
            'fields': ('date_achat',),
            'classes': ('collapse',),
        }),
    )
    
    def player_display(self, obj):
        return format_html('<span class="ai-badge ai-badge-violet">{}</span>', obj.profil.user.username)
    player_display.short_description = 'Joueur'
    
    def item_display(self, obj):
        return format_html('<strong style="color:#F0F0F5">{}</strong>', obj.item.nom)
    item_display.short_description = 'Article'
    
    def date_display(self, obj):
        return format_html('<span style="color:#8B8BA0">{}</span>', obj.date_achat.strftime('%d/%m/%Y %H:%M'))
    date_display.short_description = 'Date d\'achat'
