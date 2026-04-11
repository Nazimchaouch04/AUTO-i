from django.contrib import admin
from django.contrib.admin import AdminSite
from django.http import JsonResponse
from django.utils.html import format_html
from django.urls import path, re_path
from django.template.response import TemplateResponse
from django.db.models import Count

class CustomAdminSite(AdminSite):
    site_header = "AutoIntel Admin Dashboard"
    site_title = "AutoIntel Admin"
    index_title = "Bienvenue dans le tableau de bord AutoIntel"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('stats/', self.admin_view(self.stats_view), name='stats'),
        ]
        return custom_urls + urls

    def stats_view(self, request):
        context = {
            'total_annonces': Annonce.objects.count(),
            'annonces_actives': Annonce.objects.filter(est_active=True).count(),
            'bonnes_affaires': Annonce.objects.filter(est_bonne_affaire=True).count(),
            'total_users': UserProfile.objects.count(),
            'users_pro': Abonnement.objects.filter(plan__nom='pro').count(),
            'total_xp': ProfilJoueur.objects.aggregate(total=Count('xp'))['total'] or 0,
        }
        return TemplateResponse(request, 'admin/stats.html', context)

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        stats = {
            'total_annonces': Annonce.objects.count(),
            'bonnes_affaires': Annonce.objects.filter(est_bonne_affaire=True).count(),
            'users_actifs': UserProfile.objects.count(),
        }
        extra_context['stats'] = stats
        return super().index(request, extra_context)

# Utilisation
admin_site = CustomAdminSite(name='AutoIntelAdmin')

# Enregistrement des modèles ici si besoin
from apps.annonces.admin import VehiculeAdmin, AnnonceAdmin
admin_site.register(Annonce, AnnonceAdmin)
