from django.urls import path
from .views import (
    CanauxNotificationView,
    VerifierCanalView,
    SupprimerCanalView,
    ActiverCanalView,
    NotificationStatusView,
    HistoriqueNotificationsView,
    NotificationsRootView
)

urlpatterns = [
    path('', NotificationsRootView.as_view(), name='notifications_root'),
    path('canaux/', CanauxNotificationView.as_view(), name='canaux_notification'),
    path('canaux/<int:canal_id>/verifier/', VerifierCanalView.as_view(), name='verifier_canal'),
    path('canaux/<int:canal_id>/supprimer/', SupprimerCanalView.as_view(), name='supprimer_canal'),
    path('canaux/<int:canal_id>/activer/', ActiverCanalView.as_view(), name='activer_canal'),
    path('status/', NotificationStatusView.as_view(), name='notification_status'),
    path('historique/', HistoriqueNotificationsView.as_view(), name='historique_notifications'),
]
