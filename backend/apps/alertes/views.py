from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import Alerte
from .serializers import AlerteSerializer
from apps.subscriptions.models import Abonnement


class AlerteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AlerteSerializer

    def get_queryset(self):
        return Alerte.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        
        # Vérification de la limite (Free = 2 alertes max)
        try:
            abonnement = Abonnement.objects.get(user=user)
            est_pro = abonnement.plan.nom.lower() == 'pro'
        except Abonnement.DoesNotExist:
            est_pro = False

        if not est_pro:
            count = Alerte.objects.filter(user=user, est_active=True).count()
            if count >= 2:
                raise ValidationError({
                    "detail": "Limite d'alertes atteinte (2 max pour le plan Free). Passez Pro pour une veille illimitée !"
                })

        serializer.save(user=user)
