from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.utils import timezone
from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task
def envoyer_newsletter_hebdomadaire(user_id):
    \"\"\"Tâche Celery - Newsletter hebdomadaire personnalisée\"\"\"

    from apps.users.models import User
    from apps.annonces.models import Annonce
    from apps.gamification.models import Player
    from apps.rapports.models import RapportPDF
    from apps.dashboard.views import DashboardViewSet

    try:
        user = User.objects.get(id=user_id)
        player = getattr(user, 'player', None)

        # Bonnes affaires récentes
        bonnes_affaires = Annonce.objects.filter(
            est_bonne_affaire=True,
            date_publication__gte=timezone.now() - timezone.timedelta(days=7)
        ).order_by('-ecart_prix')[:3]

        # Stats personnalisées
        dashboard_view = DashboardViewSet()
        user_stats = dashboard_view.user_stats({'user': user}).data

        # Nouveaux rapports disponibles
        nouveaux_rapports = RapportPDF.objects.filter(
            user=user,
            statut_paiement='en_attente',
            created_at__gte=timezone.now() - timezone.timedelta(days=7)
        )

        context = {
            'user': user,
            'xp': player.xp if player else 0,
            'autocoin_balance': player.autocoin_balance if player else 100,
            'bonnes_affaires': bonnes_affaires,
            'alertes_actives': user_stats['alertes_actives'],
            'favoris': user_stats['favoris'],
            'rapports_en_attente': nouveaux_rapports.count(),
            'site_url': 'http://localhost:5173',
        }

        subject = f"🚗 AutoIntel - Votre hebdo du {timezone.now().strftime('%d/%m/%Y')}"
        
        html_message = render_to_string('notifications/newsletter_hebdo.html', context)
        plain_message = strip_tags(html_message)

        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )

        logger.info(f"Newsletter hebdo envoyée à {user.email}")
        return f'Newsletter envoyée à {user.email}'

    except Exception as e:
        logger.error(f"Erreur newsletter {user_id}: {e}")
        return f'Erreur: {str(e)}'

def envoyer_notification_email(user, titre, message, lien=None):
    \"\"\"Envoie une notification email simple\"\"\"

    try:
        lien_html = f'<a href=\"{lien}\">Voir l\'annonce</a>' if lien else ''
        
        subject = f"🔔 AutoIntel - {titre}"
        html_message = f"""
        <div style=\"font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;\">
            <h2 style=\"color: #2563eb;\">{titre}</h2>
            <p>{message}</p>
            {lien_html}
            <hr>
            <p style=\"color: #6b7280; font-size: 12px;\">
                AutoIntel - Votre assistant automobile intelligent<br>
                <a href=\"http://localhost:5173\">autointel.dz</a>
            </p>
        </div>
        """
        plain_message = f"{titre}\n\n{message}"

        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )

        logger.info(f"Email envoyé à {user.email}: {titre}")
        return True

    except Exception as e:
        logger.error(f"Erreur email {user.email}: {e}")
        return False

