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

        abonnement = request.user.subscription
        abonnement.plan = plan
        abonnement.save()

        serializer = AbonnementSerializer(abonnement)
        return Response({'detail': f'Abonnement mis à jour à {plan.get_nom_display()}', **serializer.data})
