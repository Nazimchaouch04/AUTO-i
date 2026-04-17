from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Q
from django.utils.safestring import mark_safe
from django.utils import timezone
import json

from .models import (
    Conversation, Message, UsageIA, UserProfileAnalysis,
    VehicleRecommendation, MarketInsight, IntentAnalysis, LearningData
)


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('titre_display', 'user_display', 'messages_count', 'last_activity', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('titre', 'user__username', 'user__email')
    ordering = ('-updated_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('user', 'titre'),
            'classes': ('wide',),
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def titre_display(self, obj):
        return format_html('<strong style="color:#F0F0F5">{}</strong>', obj.titre)
    titre_display.short_description = 'Titre'
    
    def user_display(self, obj):
        return format_html('<span class="ai-badge ai-badge-violet">{}</span>', obj.user.username)
    user_display.short_description = 'Utilisateur'
    
    def messages_count(self, obj):
        count = obj.messages.count()
        return format_html('<span class="ai-badge ai-badge-amber">{}</span>', count)
    messages_count.short_description = 'Messages'
    
    def last_activity(self, obj):
        if obj.updated_at:
            return format_html('<span style="color:#8B8BA0">{}</span>', obj.updated_at.strftime('%d/%m %H:%M'))
        return '-'
    last_activity.short_description = 'Dernière activité'


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('role', 'content', 'created_at')
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Si la conversation existe déjà
            return ('role', 'created_at')
        return self.readonly_fields


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation_display', 'role_display', 'content_preview', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('content', 'conversation__titre', 'conversation__user__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Message', {
            'fields': ('conversation', 'role', 'content'),
            'classes': ('wide',),
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    
    def conversation_display(self, obj):
        return format_html('<strong style="color:#F0F0F5">{}</strong>', obj.conversation.titre)
    conversation_display.short_description = 'Conversation'
    
    def role_display(self, obj):
        colors = {'user': 'ai-badge-teal', 'assistant': 'ai-badge-violet'}
        return format_html('<span class="ai-badge {}">{}</span>', 
                         colors.get(obj.role, 'ai-badge-gray'), 
                         obj.get_role_display())
    role_display.short_description = 'Rôle'
    
    def content_preview(self, obj):
        preview = obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
        return format_html('<span style="color:#8B8BA0">{}</span>', preview)
    content_preview.short_description = 'Contenu'


@admin.register(UsageIA)
class UsageIAAdmin(admin.ModelAdmin):
    list_display = ('user_display', 'date_display', 'messages_display', 'status_display')
    list_filter = ('date', 'messages_utilises')
    search_fields = ('user__username',)
    ordering = ('-date',)
    readonly_fields = ('date',)
    
    fieldsets = (
        ('Utilisation', {
            'fields': ('user', 'messages_utilises'),
            'classes': ('wide',),
        }),
        ('Métadonnées', {
            'fields': ('date',),
            'classes': ('collapse',),
        }),
    )
    
    def user_display(self, obj):
        return format_html('<span class="ai-badge ai-badge-violet">{}</span>', obj.user.username)
    user_display.short_description = 'Utilisateur'
    
    def date_display(self, obj):
        return format_html('<span style="color:#8B8BA0">{}</span>', obj.date.strftime('%d/%m/%Y'))
    date_display.short_description = 'Date'
    
    def messages_display(self, obj):
        if obj.messages_utilises == 0:
            return format_html('<span style="color:#55556A">{}</span>', obj.messages_utilises)
        elif obj.messages_utilises < 10:
            return format_html('<span class="ai-badge ai-badge-green">{}</span>', obj.messages_utilises)
        else:
            return format_html('<span class="ai-badge ai-badge-amber">{}</span>', obj.messages_utilises)
    messages_display.short_description = 'Messages'
    
    def status_display(self, obj):
        if obj.messages_utilises == 0:
            return format_html('<span class="ai-badge ai-badge-gray">Inactif</span>')
        elif obj.messages_utilises < 10:
            return format_html('<span class="ai-badge ai-badge-green">Normal</span>')
        else:
            return format_html('<span class="ai-badge ai-badge-red">Élevé</span>')
    status_display.short_description = 'Statut'


@admin.register(UserProfileAnalysis)
class UserProfileAnalysisAdmin(admin.ModelAdmin):
    list_display = ('user_display', 'budget_display', 'usage_display', 'scores_display', 'updated_at')
    list_filter = ('usage_principal', 'transmission_preferree', 'created_at')
    search_fields = ('user__username', 'user__email')
    ordering = ('-updated_at',)
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('marques_preferrees',)  # ManyToMany field correct name
    
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',),
            'classes': ('wide',),
        }),
        ('Préférences budget', {
            'fields': (('budget_min', 'budget_max'),),
            'classes': ('wide',),
        }),
        ('Préférences véhicule', {
            'fields': ('marques_preferrees', 'types_vehicule', 'usage_principal'),
            'classes': ('wide',),
        }),
        ('Caractéristiques', {
            'fields': (('kilometrage_annuel', 'preferences_carburant'), 
                      ('places_minimales', 'porte_minimales'), 
                      'transmission_preferree'),
            'classes': ('wide',),
        }),
        ('Scores IA', {
            'fields': (('score_ecologique', 'score_budget', 'score_praticite'),),
            'classes': ('wide',),
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def user_display(self, obj):
        return format_html('<span class="ai-badge ai-badge-violet">{}</span>', obj.user.username)
    user_display.short_description = 'Utilisateur'
    
    def budget_display(self, obj):
        if obj.budget_max:
            return format_html('<span style="color:#F59E0B">{:,} DA</span>', int(obj.budget_max))
        return '-'
    budget_display.short_description = 'Budget max'
    
    def usage_display(self, obj):
        return format_html('<span class="ai-badge ai-badge-teal">{}</span>', obj.get_usage_principal_display())
    usage_display.short_description = 'Usage principal'
    
    def scores_display(self, obj):
        return format_html(
            '<span style="color:#6C63FF">É:{}</span> | '
            '<span style="color:#F59E0B">B:{}</span> | '
            '<span style="color:#00D4AA">P:{}</span>',
            obj.score_ecologique, obj.score_budget, obj.score_praticite
        )
    scores_display.short_description = 'Scores'


@admin.register(VehicleRecommendation)
class VehicleRecommendationAdmin(admin.ModelAdmin):
    list_display = ('user_display', 'vehicule_display', 'score_display', 'confidence_display', 'created_at')
    list_filter = ('score_total', 'confiance_prediction', 'created_at')
    search_fields = ('user__username', 'vehicule__marque', 'vehicule__modele')
    ordering = ('-score_total', '-created_at')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Recommandation', {
            'fields': ('user', 'vehicule', 'conversation'),
            'classes': ('wide',),
        }),
        ('Scores', {
            'fields': (('score_total', 'score_prix', 'score_besoins'), 
                      ('score_marche', 'score_disponibilite')),
            'classes': ('wide',),
        }),
        ('Prédictions prix', {
            'fields': (('prix_estime_1an', 'prix_estime_3ans'), 'confiance_prediction'),
            'classes': ('wide',),
        }),
        ('Justifications IA', {
            'fields': ('raisons_recommandation', 'points_forts', 'points_faibles'),
            'classes': ('wide',),
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    
    def user_display(self, obj):
        return format_html('<span class="ai-badge ai-badge-violet">{}</span>', obj.user.username)
    user_display.short_description = 'Utilisateur'
    
    def vehicule_display(self, obj):
        return format_html('<strong style="color:#F0F0F5">{} {}</strong>', 
                         obj.vehicule.marque, obj.vehicule.modele)
    vehicule_display.short_description = 'Véhicule'
    
    def score_display(self, obj):
        if obj.score_total >= 80:
            return format_html('<span class="ai-badge ai-badge-teal">{}</span>', obj.score_total)
        elif obj.score_total >= 60:
            return format_html('<span class="ai-badge ai-badge-amber">{}</span>', obj.score_total)
        else:
            return format_html('<span class="ai-badge ai-badge-gray">{}</span>', obj.score_total)
    score_display.short_description = 'Score total'
    
    def confidence_display(self, obj):
        if obj.confiance_prediction >= 80:
            return format_html('<span style="color:#00D4AA">{}</span>', obj.confiance_prediction)
        elif obj.confiance_prediction >= 60:
            return format_html('<span style="color:#F59E0B">{}</span>', obj.confiance_prediction)
        else:
            return format_html('<span style="color:#8B8BA0">{}</span>', obj.confiance_prediction)
    confidence_display.short_description = 'Confiance'


@admin.register(MarketInsight)
class MarketInsightAdmin(admin.ModelAdmin):
    list_display = ('titre_display', 'type_display', 'impact_display', 'confidence_display', 'validity_display')
    list_filter = ('type_insight', 'niveau_impact', 'confiance', 'created_at')
    search_fields = ('titre', 'description')
    ordering = ('-niveau_impact', '-created_at')
    readonly_fields = ('created_at',)
    filter_horizontal = ('marques_concernees',)
    
    fieldsets = (
        ('Insight marché', {
            'fields': ('titre', 'description', 'type_insight'),
            'classes': ('wide',),
        }),
        ('Données associées', {
            'fields': ('marques_concernees', 'categories_vehicules', 'fourchettes_prix'),
            'classes': ('wide',),
        }),
        ('Impact et confiance', {
            'fields': (('niveau_impact', 'confiance'),),
            'classes': ('wide',),
        }),
        ('Période de validité', {
            'fields': ('date_debut', 'date_fin'),
            'classes': ('wide',),
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    
    def titre_display(self, obj):
        return format_html('<strong style="color:#F0F0F5">{}</strong>', obj.titre[:50] + '...' if len(obj.titre) > 50 else obj.titre)
    titre_display.short_description = 'Titre'
    
    def type_display(self, obj):
        colors = {
            'tendance_prix': 'ai-badge-violet',
            'opportunite': 'ai-badge-teal',
            'alerte_marche': 'ai-badge-red',
            'conseil_achat': 'ai-badge-amber',
            'conseil_vente': 'ai-badge-green',
            'prediction': 'ai-badge-gray',
        }
        return format_html('<span class="ai-badge {}">{}</span>', 
                         colors.get(obj.type_insight, 'ai-badge-gray'), 
                         obj.get_type_insight_display())
    type_display.short_description = 'Type'
    
    def impact_display(self, obj):
        if obj.niveau_impact >= 80:
            return format_html('<span class="ai-badge ai-badge-red">{}</span>', obj.niveau_impact)
        elif obj.niveau_impact >= 60:
            return format_html('<span class="ai-badge ai-badge-amber">{}</span>', obj.niveau_impact)
        else:
            return format_html('<span class="ai-badge ai-badge-gray">{}</span>', obj.niveau_impact)
    impact_display.short_description = 'Impact'
    
    def confidence_display(self, obj):
        return format_html('<span style="color:#6C63FF">{}</span>', obj.confiance)
    confidence_display.short_description = 'Confiance'
    
    def validity_display(self, obj):
        if obj.date_fin and obj.date_fin < timezone.now():
            return format_html('<span class="ai-badge ai-badge-gray">Expiré</span>')
        return format_html('<span class="ai-badge ai-badge-green">Actif</span>')
    validity_display.short_description = 'Validité'


@admin.register(IntentAnalysis)
class IntentAnalysisAdmin(admin.ModelAdmin):
    list_display = ('message_display', 'intent_display', 'sentiment_display', 'urgency_display', 'created_at')
    list_filter = ('intent_principale', 'sentiment', 'niveau_urgence')
    search_fields = ('message__content', 'message__conversation__user__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'message')
    
    fieldsets = (
        ('Analyse d\'intention', {
            'fields': ('message', 'intent_principale', 'sentiment', 'niveau_urgence'),
            'classes': ('wide',),
        }),
        ('Entités extraites', {
            'fields': ('entites',),
            'classes': ('wide',),
        }),
        ('Contexte', {
            'fields': ('contexte_conversation',),
            'classes': ('wide',),
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    
    def message_display(self, obj):
        preview = obj.message.content[:50] + '...' if len(obj.message.content) > 50 else obj.message.content
        return format_html('<span style="color:#8B8BA0">{}</span>', preview)
    message_display.short_description = 'Message'
    
    def intent_display(self, obj):
        colors = {
            'recherche_vehicule': 'ai-badge-violet',
            'conseil_achat': 'ai-badge-teal',
            'estimation_prix': 'ai-badge-amber',
            'information_marche': 'ai-badge-green',
            'comparaison': 'ai-badge-red',
            'avis_expert': 'ai-badge-gray',
        }
        return format_html('<span class="ai-badge {}">{}</span>', 
                         colors.get(obj.intent_principale, 'ai-badge-gray'), 
                         obj.get_intent_principale_display())
    intent_display.short_description = 'Intention'
    
    def sentiment_display(self, obj):
        colors = {
            'positif': 'ai-badge-green',
            'neutre': 'ai-badge-gray',
            'negatif': 'ai-badge-red',
        }
        return format_html('<span class="ai-badge {}">{}</span>', 
                         colors.get(obj.sentiment, 'ai-badge-gray'), 
                         obj.get_sentiment_display())
    sentiment_display.short_description = 'Sentiment'
    
    def urgency_display(self, obj):
        if obj.niveau_urgence >= 80:
            return format_html('<span class="ai-badge ai-badge-red">{}</span>', obj.niveau_urgence)
        elif obj.niveau_urgence >= 50:
            return format_html('<span class="ai-badge ai-badge-amber">{}</span>', obj.niveau_urgence)
        else:
            return format_html('<span class="ai-badge ai-badge-gray">{}</span>', obj.niveau_urgence)
    urgency_display.short_description = 'Urgence'


@admin.register(LearningData)
class LearningDataAdmin(admin.ModelAdmin):
    list_display = ('type_display', 'user_display', 'performance_display', 'created_at')
    list_filter = ('type_donnee', 'performance_score', 'created_at')
    search_fields = ('user__username', 'feedback_utilisateur')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Donnée apprentissage', {
            'fields': ('user', 'type_donnee', 'performance_score'),
            'classes': ('wide',),
        }),
        ('Données', {
            'fields': ('donnees_entree', 'donnees_sortie'),
            'classes': ('wide',),
        }),
        ('Feedback', {
            'fields': ('feedback_utilisateur',),
            'classes': ('wide',),
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    
    def type_display(self, obj):
        colors = {
            'conversation': 'ai-badge-violet',
            'recommandation_feedback': 'ai-badge-teal',
            'prediction_resultat': 'ai-badge-amber',
            'comportement_recherche': 'ai-badge-green',
        }
        return format_html('<span class="ai-badge {}">{}</span>', 
                         colors.get(obj.type_donnee, 'ai-badge-gray'), 
                         obj.get_type_donnee_display())
    type_display.short_description = 'Type'
    
    def user_display(self, obj):
        if obj.user:
            return format_html('<span class="ai-badge ai-badge-violet">{}</span>', obj.user.username)
        return format_html('<span class="ai-badge ai-badge-gray">Système</span>')
    user_display.short_description = 'Utilisateur'
    
    def performance_display(self, obj):
        if obj.performance_score is None:
            return format_html('<span style="color:#55556A">—</span>')
        elif obj.performance_score >= 80:
            return format_html('<span class="ai-badge ai-badge-teal">{}</span>', obj.performance_score)
        elif obj.performance_score >= 60:
            return format_html('<span class="ai-badge ai-badge-amber">{}</span>', obj.performance_score)
        else:
            return format_html('<span class="ai-badge ai-badge-red">{}</span>', obj.performance_score)
    performance_display.short_description = 'Performance'
