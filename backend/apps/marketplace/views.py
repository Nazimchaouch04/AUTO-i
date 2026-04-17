from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from .models import Listing, Transaction, SellerProfile, Review, Favorite, Message
from .serializers import (
    ListingSerializer,
    ListingCreateSerializer,
    TransactionSerializer,
    SellerProfileSerializer,
    ReviewSerializer,
    FavoriteSerializer,
    MessageSerializer,
)


class MarketplaceRootView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        base = '/api/marketplace/'
        return Response({
            'message': 'Marketplace automobile AutoIntel',
            'listings': f'{base}listings/',
            'profile': f'{base}profile/',
            'transactions': f'{base}transactions/',
            'favorites': f'{base}favorites/',
            'reviews': f'{base}reviews/',
            'messages': f'{base}messages/',
        })


class ListingViewSet(viewsets.ModelViewSet):
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Listing.objects.select_related('seller').all()

    def get_serializer_class(self):
        if self.action == 'create':
            return ListingCreateSerializer
        return ListingSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.GET.get('q', '')
        brand = request.GET.get('brand', '')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        queryset = self.get_queryset()

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(brand__icontains=query) |
                Q(model__icontains=query)
            )

        if brand:
            queryset = queryset.filter(brand__icontains=brand)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        listing = self.get_object()
        user = request.user

        favorite, created = Favorite.objects.get_or_create(
            user=user, listing=listing
        )

        if not created:
            favorite.delete()
            return Response({'status': 'removed from favorites'})
        
        return Response({'status': 'added to favorites'})


class SellerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = SellerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SellerProfile.objects.select_related('user').all()

    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        profile, created = SellerProfile.objects.get_or_create(
            user=request.user
        )
        
        if request.method == 'PATCH':
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(
            Q(buyer=user) | Q(seller__user=user)
        ).select_related('listing', 'buyer', 'seller__user')

    @action(detail=True, methods=['post'])
    def create_order(self, request, pk=None):
        listing = self.get_object()
        buyer = request.user

        if listing.seller.user == buyer:
            return Response(
                {'error': 'Cannot buy your own listing'},
                status=status.HTTP_400_BAD_REQUEST
            )

        transaction = Transaction.objects.create(
            listing=listing,
            buyer=buyer,
            seller=listing.seller,
            total_amount=listing.price,
            status='pending'
        )

        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(
            reviewer=self.request.user
        ).select_related('transaction', 'reviewed')

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)


class FavoriteViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(
            user=self.request.user
        ).select_related('listing')


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(
            Q(sender=user) | Q(recipient=user)
        ).select_related('listing', 'sender', 'recipient')

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
