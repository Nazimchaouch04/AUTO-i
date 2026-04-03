import time
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Plan, Abonnement
from .serializers import PlanSerializer, AbonnementSerializer


class PlanViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer


class AbonnementViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def mon_abonnement(self, request):
        abonnement = request.user.subscription
        serializer = AbonnementSerializer(abonnement)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def upgrade(self, request):
        plan_nom = request.data.get('plan')
        try:
            plan = Plan.objects.get(nom=plan_nom)
        except Plan.DoesNotExist:
            return Response({'error': 'Plan non trouvé'}, status=status.HTTP_404_NOT_FOUND)

        # Simulation de paiement (delay 2s)
        time.sleep(2)

        abonnement = request.user.subscription
        abonnement.plan = plan
        abonnement.save()

        # Ici, dans un vrai système, on mettrait à jour stripe_subscription_id
        
        serializer = AbonnementSerializer(abonnement)
        return Response({
            'detail': f'Abonnement mis à jour à {plan.get_nom_display()} avec succès !',
            'status': 'success',
            **serializer.data
        })

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def webhook(self, request):
        """
        Placeholder pour le webhook Stripe.
        Vérifiera la signature et mettra à jour l'abonnement en conséquence.
        """
        # Event Stripe verification here
        return Response({'status': 'webhook received'}, status=status.HTTP_200_OK)
