import time
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.conf import settings
from .models import Plan, Abonnement
from .serializers import PlanSerializer, AbonnementSerializer
from .stripe_service import create_checkout_session, handle_webhook

class PlanListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        plans = Plan.objects.all()
        serializer = PlanSerializer(plans, many=True)
        return Response(serializer.data)

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        plan_nom = request.data.get('plan')
        if plan_nom not in ['pro', 'business']:
            return Response({'error': 'Plan invalide'}, status=400)
        try:
            frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:5173')
            session = create_checkout_session(
                user=request.user,
                plan_nom=plan_nom,
                success_url=f'{frontend_url}/abonnement/succes',
                cancel_url=f'{frontend_url}/pricing',
            )
            return Response(session)
        except Exception as e:
            return Response({'error': str(e)}, status=400)


class StripeWebhookView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
        handle_webhook(payload, sig_header)
        return Response({'received': True})


class AbonnementActuelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        abonnement = request.user.subscription
        return Response({
            'plan': abonnement.plan.nom,
            'actif': abonnement.actif,
            'estimations_par_mois': abonnement.plan.estimations_par_mois,
            'alertes_max': abonnement.plan.alertes_max,
            'export_csv': abonnement.plan.export_csv,
            'acces_api': abonnement.plan.acces_api,
        })
