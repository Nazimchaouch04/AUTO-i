from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from .models import MarketplaceListing, MarketplaceOrder, SellerVerification
from .serializers import (
    DeliveryConfirmationSerializer,
    DisputeResolutionSerializer,
    DisputeSerializer,
    MarketplaceListingCreateSerializer,
    MarketplaceListingSerializer,
    MarketplaceOrderCreateSerializer,
    MarketplaceOrderSerializer,
    PaymentConfirmationSerializer,
    SellerVerificationReviewSerializer,
    SellerVerificationSerializer,
    ShipmentUpdateSerializer,
)
from .services import MarketplaceError, MarketplaceService


class MarketplaceRootView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        base = '/api/marketplace/'
        return Response({
            'message': 'Marketplace automobile AutoIntel',
            'verification': f'{base}verification/',
            'listings': f'{base}listings/',
            'orders': f'{base}orders/',
            'endpoints': [
                {'path': 'verification/', 'method': 'GET/POST', 'description': "Soumettre ou consulter la verification vendeur"},
                {'path': 'verification/<id>/review/', 'method': 'POST', 'description': "Approuver ou rejeter une verification vendeur"},
                {'path': 'listings/', 'method': 'GET/POST', 'description': "Lister les annonces marketplace ou publier une annonce"},
                {'path': 'listings/mine/', 'method': 'GET', 'description': "Voir ses annonces vendeur"},
                {'path': 'listings/<id>/cancel/', 'method': 'POST', 'description': "Annuler une annonce vendeur"},
                {'path': 'orders/', 'method': 'GET/POST', 'description': "Creer ou consulter ses transactions"},
                {'path': 'orders/<id>/confirm_payment/', 'method': 'POST', 'description': "Confirmer un paiement securise"},
                {'path': 'orders/<id>/ship/', 'method': 'POST', 'description': "Mettre a jour la logistique"},
                {'path': 'orders/<id>/confirm_delivery/', 'method': 'POST', 'description': "Confirmer la livraison et liberer l'escrow"},
                {'path': 'orders/<id>/open_dispute/', 'method': 'POST', 'description': "Ouvrir un litige"},
                {'path': 'orders/<id>/resolve_dispute/', 'method': 'POST', 'description': "Resoudre un litige"},
            ],
        })


class SellerVerificationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        verification = SellerVerification.objects.filter(user=request.user).first()
        if not verification:
            return Response({'detail': 'Aucune verification vendeur.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(SellerVerificationSerializer(verification).data)

    def post(self, request):
        serializer = SellerVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            verification = MarketplaceService.submit_verification(
                request.user,
                serializer.validated_data,
            )
        except MarketplaceError as exc:
            return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(SellerVerificationSerializer(verification).data, status=status.HTTP_201_CREATED)


class SellerVerificationReviewView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, verification_id):
        verification = SellerVerification.objects.filter(id=verification_id).first()
        if not verification:
            return Response({'error': 'Verification introuvable'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SellerVerificationReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            verification = MarketplaceService.review_verification(
                verification=verification,
                reviewer=request.user,
                approved=serializer.validated_data['approved'],
                review_notes=serializer.validated_data.get('review_notes', ''),
            )
        except MarketplaceError as exc:
            return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(SellerVerificationSerializer(verification).data)


class MarketplaceListingViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = MarketplaceListing.objects.select_related('seller', 'annonce__vehicule')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return MarketplaceListingCreateSerializer
        return MarketplaceListingSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == 'mine':
            return queryset.filter(seller=self.request.user)
        if self.request.user.is_authenticated and self.action in {'retrieve', 'publish', 'cancel'}:
            if self.request.user.is_staff:
                return queryset
            return queryset.filter(
                Q(status=MarketplaceListing.Status.PUBLISHED)
                | Q(seller=self.request.user)
            )
        if self.request.user.is_authenticated and self.request.query_params.get('mine') == 'true':
            return queryset.filter(seller=self.request.user)
        return queryset.filter(status=MarketplaceListing.Status.PUBLISHED)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            listing = MarketplaceService.create_listing(request.user, serializer.validated_data)
        except MarketplaceError as exc:
            return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        response_serializer = MarketplaceListingSerializer(listing, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        listing = self.get_object()
        if listing.status != MarketplaceListing.Status.PUBLISHED and (
            not request.user.is_authenticated
            or (request.user.id != listing.seller_id and not request.user.is_staff)
        ):
            return Response({'error': 'Annonce indisponible'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MarketplaceListingSerializer(listing, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def mine(self, request):
        serializer = MarketplaceListingSerializer(
            self.get_queryset(),
            many=True,
            context={'request': request},
        )
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def publish(self, request, pk=None):
        listing = self.get_object()
        try:
            listing = MarketplaceService.publish_listing(listing, request.user)
        except MarketplaceError as exc:
            return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(MarketplaceListingSerializer(listing, context={'request': request}).data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def cancel(self, request, pk=None):
        listing = self.get_object()
        try:
            listing = MarketplaceService.cancel_listing(listing, request.user)
        except MarketplaceError as exc:
            return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(MarketplaceListingSerializer(listing, context={'request': request}).data)


class MarketplaceOrderViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = MarketplaceOrder.objects.select_related(
        'listing__annonce__vehicule',
        'buyer',
        'seller',
        'escrow',
        'shipment',
    ).prefetch_related('payments')
    serializer_class = MarketplaceOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        role = self.request.query_params.get('role')
        if role == 'seller':
            return self.queryset.filter(seller=self.request.user)
        return self.queryset.filter(
            Q(buyer=self.request.user) | Q(seller=self.request.user)
        ).distinct()

    def create(self, request, *args, **kwargs):
        serializer = MarketplaceOrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        listing = MarketplaceListing.objects.select_related('annonce__vehicule', 'seller').filter(
            id=serializer.validated_data['listing_id']
        ).first()
        if not listing:
            return Response({'error': 'Annonce marketplace introuvable'}, status=status.HTTP_404_NOT_FOUND)

        try:
            order = MarketplaceService.create_order(
                buyer=request.user,
                listing=listing,
                payload=serializer.validated_data,
            )
        except MarketplaceError as exc:
            return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        response_serializer = MarketplaceOrderSerializer(order, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def confirm_payment(self, request, pk=None):
        order = self.get_object()
        serializer = PaymentConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            order = MarketplaceService.confirm_payment(
                order=order,
                actor=request.user,
                provider_reference=serializer.validated_data.get('provider_reference'),
            )
        except MarketplaceError as exc:
            return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(MarketplaceOrderSerializer(order, context={'request': request}).data)

    @action(detail=True, methods=['post'])
    def ship(self, request, pk=None):
        order = self.get_object()
        serializer = ShipmentUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            order = MarketplaceService.mark_shipped(order, request.user, serializer.validated_data)
        except MarketplaceError as exc:
            return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(MarketplaceOrderSerializer(order, context={'request': request}).data)

    @action(detail=True, methods=['post'])
    def confirm_delivery(self, request, pk=None):
        order = self.get_object()
        serializer = DeliveryConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            order = MarketplaceService.confirm_delivery(
                order=order,
                buyer=request.user,
                release_token=serializer.validated_data['release_token'],
            )
        except MarketplaceError as exc:
            return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(MarketplaceOrderSerializer(order, context={'request': request}).data)

    @action(detail=True, methods=['post'])
    def open_dispute(self, request, pk=None):
        order = self.get_object()
        serializer = DisputeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            order = MarketplaceService.open_dispute(
                order=order,
                actor=request.user,
                reason=serializer.validated_data['reason'],
            )
        except MarketplaceError as exc:
            return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(MarketplaceOrderSerializer(order, context={'request': request}).data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def resolve_dispute(self, request, pk=None):
        order = self.get_object()
        serializer = DisputeResolutionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            order = MarketplaceService.resolve_dispute(
                order=order,
                reviewer=request.user,
                decision=serializer.validated_data['decision'],
                notes=serializer.validated_data.get('notes', ''),
            )
        except MarketplaceError as exc:
            return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(MarketplaceOrderSerializer(order, context={'request': request}).data)
