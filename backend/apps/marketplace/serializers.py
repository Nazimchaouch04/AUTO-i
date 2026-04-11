from rest_framework import serializers

from apps.annonces.models import Annonce

from .models import (
    EscrowAccount,
    LogisticsShipment,
    MarketplaceListing,
    MarketplaceOrder,
    MarketplacePayment,
    SellerVerification,
)


class SellerVerificationSerializer(serializers.ModelSerializer):
    document_number = serializers.CharField(write_only=True, required=True)
    is_verified = serializers.BooleanField(read_only=True)

    class Meta:
        model = SellerVerification
        fields = [
            'id',
            'status',
            'legal_name',
            'phone_number',
            'country',
            'city',
            'address_line',
            'document_type',
            'document_number',
            'document_number_last4',
            'document_front_url',
            'document_back_url',
            'selfie_url',
            'business_name',
            'tax_id',
            'review_notes',
            'risk_score',
            'submitted_at',
            'reviewed_at',
            'verified_at',
            'is_verified',
            'metadata',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'status',
            'document_number_last4',
            'review_notes',
            'risk_score',
            'submitted_at',
            'reviewed_at',
            'verified_at',
            'created_at',
            'updated_at',
        ]


class SellerVerificationReviewSerializer(serializers.Serializer):
    approved = serializers.BooleanField()
    review_notes = serializers.CharField(required=False, allow_blank=True)


class VehiclePayloadSerializer(serializers.Serializer):
    marque = serializers.CharField(max_length=100)
    modele = serializers.CharField(max_length=100)
    categorie = serializers.CharField(max_length=50, required=False, allow_blank=True)


class ListingAnnoncePayloadSerializer(serializers.Serializer):
    annee = serializers.IntegerField(min_value=1900)
    kilometrage = serializers.IntegerField(min_value=0)
    carburant = serializers.CharField(max_length=20)
    boite = serializers.CharField(max_length=20)
    puissance = serializers.IntegerField(required=False, allow_null=True)
    prix = serializers.DecimalField(max_digits=10, decimal_places=2)
    ville = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    pays = serializers.CharField(max_length=5, required=False)
    description = serializers.CharField(required=False, allow_blank=True)
    url_originale = serializers.URLField(required=False, allow_blank=True, allow_null=True)


class MarketplaceListingCreateSerializer(serializers.Serializer):
    vehicule = VehiclePayloadSerializer()
    annonce = ListingAnnoncePayloadSerializer()
    logistics_mode = serializers.ChoiceField(
        choices=MarketplaceListing.LogisticsMode.choices,
        default=MarketplaceListing.LogisticsMode.PLATFORM,
    )
    secure_payment_required = serializers.BooleanField(default=True)
    escrow_required = serializers.BooleanField(default=True)
    logistics_enabled = serializers.BooleanField(default=True)
    marketplace_fee_pct = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
    )
    escrow_window_days = serializers.IntegerField(required=False, min_value=1, max_value=30)
    metadata = serializers.JSONField(required=False)


class MarketplaceListingSerializer(serializers.ModelSerializer):
    seller_username = serializers.CharField(source='seller.username', read_only=True)
    annonce_details = serializers.SerializerMethodField()

    class Meta:
        model = MarketplaceListing
        fields = [
            'id',
            'seller',
            'seller_username',
            'status',
            'logistics_mode',
            'secure_payment_required',
            'escrow_required',
            'logistics_enabled',
            'marketplace_fee_pct',
            'escrow_window_days',
            'verification_snapshot',
            'published_at',
            'sold_at',
            'cancelled_at',
            'metadata',
            'created_at',
            'updated_at',
            'annonce_details',
        ]
        read_only_fields = fields

    def get_annonce_details(self, obj):
        annonce = obj.annonce
        return {
            'id': annonce.id,
            'vehicule_id': annonce.vehicule_id,
            'marque': annonce.vehicule.marque,
            'modele': annonce.vehicule.modele,
            'categorie': annonce.vehicule.categorie,
            'annee': annonce.annee,
            'kilometrage': annonce.kilometrage,
            'carburant': annonce.carburant,
            'boite': annonce.boite,
            'puissance': annonce.puissance,
            'prix': annonce.prix,
            'ville': annonce.ville,
            'pays': annonce.pays,
            'description': annonce.description,
            'source': annonce.source,
            'est_active': annonce.est_active,
        }


class MarketplaceOrderCreateSerializer(serializers.Serializer):
    listing_id = serializers.IntegerField()
    currency = serializers.CharField(max_length=10, required=False, default='EUR')
    logistics_required = serializers.BooleanField(required=False)
    shipping_address = serializers.JSONField(required=False)
    pickup_address = serializers.CharField(required=False, allow_blank=True)
    buyer_note = serializers.CharField(required=False, allow_blank=True)
    delivery_note = serializers.CharField(required=False, allow_blank=True)


class MarketplacePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketplacePayment
        fields = [
            'id',
            'provider',
            'status',
            'amount',
            'currency',
            'provider_reference',
            'client_secret',
            'provider_payload',
            'confirmed_at',
            'refunded_at',
            'created_at',
        ]
        read_only_fields = fields


class EscrowAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = EscrowAccount
        fields = [
            'id',
            'status',
            'held_amount',
            'funded_at',
            'released_at',
            'refunded_at',
            'disputed_at',
            'dispute_notes',
            'created_at',
        ]
        read_only_fields = fields


class LogisticsShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogisticsShipment
        fields = [
            'id',
            'status',
            'provider',
            'tracking_number',
            'pickup_address',
            'destination_address',
            'shipped_at',
            'delivered_at',
            'notes',
            'metadata',
            'created_at',
        ]
        read_only_fields = fields


class PaymentConfirmationSerializer(serializers.Serializer):
    provider_reference = serializers.CharField(required=False, allow_blank=True)


class ShipmentUpdateSerializer(serializers.Serializer):
    provider = serializers.CharField(required=False, allow_blank=True)
    tracking_number = serializers.CharField(required=False, allow_blank=True)
    notes = serializers.CharField(required=False, allow_blank=True)


class DeliveryConfirmationSerializer(serializers.Serializer):
    release_token = serializers.CharField()


class DisputeSerializer(serializers.Serializer):
    reason = serializers.CharField()


class DisputeResolutionSerializer(serializers.Serializer):
    decision = serializers.ChoiceField(choices=['release_to_seller', 'refund_buyer'])
    notes = serializers.CharField(required=False, allow_blank=True)


class MarketplaceOrderSerializer(serializers.ModelSerializer):
    buyer_username = serializers.CharField(source='buyer.username', read_only=True)
    seller_username = serializers.CharField(source='seller.username', read_only=True)
    listing = MarketplaceListingSerializer(read_only=True)
    payments = MarketplacePaymentSerializer(many=True, read_only=True)
    escrow = EscrowAccountSerializer(read_only=True)
    shipment = LogisticsShipmentSerializer(read_only=True)
    escrow_release_token = serializers.SerializerMethodField()

    class Meta:
        model = MarketplaceOrder
        fields = [
            'id',
            'reference',
            'listing',
            'buyer',
            'buyer_username',
            'seller',
            'seller_username',
            'status',
            'currency',
            'vehicle_price',
            'marketplace_fee',
            'logistics_fee',
            'escrow_amount',
            'total_amount',
            'secure_payment_required',
            'escrow_required',
            'logistics_required',
            'shipping_address',
            'buyer_note',
            'dispute_reason',
            'created_at',
            'updated_at',
            'payments',
            'escrow',
            'shipment',
            'escrow_release_token',
        ]
        read_only_fields = fields

    def get_escrow_release_token(self, obj):
        request = self.context.get('request')
        token = getattr(obj, '_issued_release_token', None)
        if token and request and request.user.is_authenticated and request.user.id == obj.buyer_id:
            return token
        return None
