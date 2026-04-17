from rest_framework import serializers
from django.contrib.auth.models import User

from apps.annonces.models import Annonce

from .models import (
    Listing,
    Transaction,
    SellerProfile,
    Review,
    Favorite,
    Message,
)


class SellerProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = SellerProfile
        fields = [
            'id', 'user', 'username', 'email', 'company_name', 
            'phone_number', 'description', 'is_verified', 
            'total_sales', 'average_rating', 'created_at'
        ]
        read_only_fields = ['total_sales', 'average_rating', 'created_at']


class ListingSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source='seller.user.username', read_only=True)
    seller_company = serializers.CharField(source='seller.company_name', read_only=True)

    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'brand', 'model', 'year', 'price', 
            'mileage', 'fuel_type', 'transmission', 'description',
            'seller', 'seller_name', 'seller_company', 'status',
            'created_at'
        ]
        read_only_fields = ['created_at']


class ListingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = [
            'title', 'brand', 'model', 'year', 'price', 
            'mileage', 'fuel_type', 'transmission', 'description'
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        seller_profile, created = SellerProfile.objects.get_or_create(user=user)
        validated_data['seller'] = seller_profile
        return Listing.objects.create(**validated_data)


class TransactionSerializer(serializers.ModelSerializer):
    listing_title = serializers.CharField(source='listing.title', read_only=True)
    seller_name = serializers.CharField(source='seller.user.username', read_only=True)
    buyer_name = serializers.CharField(source='buyer.username', read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id', 'listing', 'listing_title', 'buyer', 'seller',
            'seller_name', 'buyer_name', 'total_amount', 'status',
            'created_at'
        ]
        read_only_fields = ['total_amount', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source='reviewer.username', read_only=True)
    reviewed_name = serializers.CharField(source='reviewed.user.username', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'transaction', 'reviewer', 'reviewed',
            'reviewer_name', 'reviewed_name', 'rating', 'comment',
            'created_at'
        ]
        read_only_fields = ['created_at']


class FavoriteSerializer(serializers.ModelSerializer):
    listing_title = serializers.CharField(source='listing.title', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Favorite
        fields = [
            'id', 'user', 'user_name', 'listing', 'listing_title', 'created_at'
        ]
        read_only_fields = ['created_at']


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)
    recipient_name = serializers.CharField(source='recipient.username', read_only=True)
    listing_title = serializers.CharField(source='listing.title', read_only=True)

    class Meta:
        model = Message
        fields = [
            'id', 'transaction', 'listing', 'listing_title',
            'sender', 'sender_name', 'recipient', 'recipient_name',
            'subject', 'content', 'is_read', 'created_at'
        ]
        read_only_fields = ['created_at']
