import secrets
import uuid
from decimal import Decimal

from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from apps.annonces.models import Annonce


class SellerVerification(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Brouillon'
        SUBMITTED = 'submitted', 'Soumise'
        APPROVED = 'approved', 'Approuvee'
        REJECTED = 'rejected', 'Rejetee'

    class DocumentType(models.TextChoices):
        NATIONAL_ID = 'national_id', 'Carte nationale'
        PASSPORT = 'passport', 'Passeport'
        DRIVER_LICENSE = 'driver_license', 'Permis de conduire'
        BUSINESS_REGISTRATION = 'business_registration', 'Registre commercial'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='seller_verification',
        unique=True
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    legal_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=30)
    country = models.CharField(max_length=5, default='DZ')
    city = models.CharField(max_length=100, blank=True)
    address_line = models.CharField(max_length=255)
    document_type = models.CharField(max_length=30, choices=DocumentType.choices)
    document_number_last4 = models.CharField(max_length=4)
    document_front_url = models.URLField(blank=True)
    document_back_url = models.URLField(blank=True)
    selfie_url = models.URLField(blank=True)
    business_name = models.CharField(max_length=200, blank=True)
    tax_id = models.CharField(max_length=100, blank=True)
    review_notes = models.TextField(blank=True)
    risk_score = models.PositiveSmallIntegerField(default=50)
    submitted_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='seller_verifications_reviewed',
    )
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"KYC {self.user.username} - {self.status}"

    @property
    def is_verified(self):
        return self.status == self.Status.APPROVED


class MarketplaceListing(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Brouillon'
        PUBLISHED = 'published', 'Publiée'
        RESERVED = 'reserved', 'Réservée'
        SOLD = 'sold', 'Vendue'
        CANCELLED = 'cancelled', 'Annulée'

    class LogisticsMode(models.TextChoices):
        PLATFORM = 'platform', 'Logistique marketplace'
        SELLER = 'seller', 'Expédition vendeur'
        PICKUP = 'pickup', 'Retrait sur place'

    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='marketplace_listings',
    )
    annonce = models.OneToOneField(
        Annonce,
        on_delete=models.CASCADE,
        related_name='marketplace_listing',
    )
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    
    # Informations véhicule
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    mileage = models.IntegerField()
    fuel_type = models.CharField(max_length=20)
    transmission = models.CharField(max_length=20)
    color = models.CharField(max_length=50)
    doors = models.IntegerField()
    seats = models.IntegerField()
    
    # Prix
    price = models.DecimalField(max_digits=12, decimal_places=2)
    is_negotiable = models.BooleanField(default=False)
    
    # Médias
    main_image = models.ImageField(upload_to='marketplace_images/')
    additional_images = models.JSONField(default=list)
    
    # Localisation
    location = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    
    # État et statut
    condition = models.CharField(max_length=20)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    
    # Options et équipements
    features = models.JSONField(default=list)
    maintenance_history = models.JSONField(default=list)
    inspection_report = models.FileField(upload_to='inspection_reports/', null=True, blank=True)
    
    # Visibilité
    is_featured = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)
    favorites_count = models.IntegerField(default=0)
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Annonce marketplace"
        verbose_name_plural = "Annonces marketplace"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.brand} {self.model} - {self.year}"
    secure_payment_required = models.BooleanField(default=True)
    escrow_required = models.BooleanField(default=True)
    logistics_enabled = models.BooleanField(default=True)
    marketplace_fee_pct = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('5.00'),
    )
    escrow_window_days = models.PositiveSmallIntegerField(default=7)
    verification_snapshot = models.CharField(max_length=20, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    sold_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return f"Listing {self.annonce_id} - {self.status}"


class MarketplaceOrder(models.Model):
    class Status(models.TextChoices):
        INITIATED = 'initiated', 'Initié'
        PAYMENT_PENDING = 'payment_pending', 'Paiement en attente'
        ESCROW_FUNDED = 'escrow_funded', 'Escrow alimenté'
        PROCESSING = 'processing', 'Préparation'
        IN_TRANSIT = 'in_transit', 'En transit'
        DELIVERED = 'delivered', 'Livrée'
        COMPLETED = 'completed', 'Complété'
        DISPUTED = 'disputed', 'En litige'
        CANCELLED = 'cancelled', 'Annulé'
        REFUNDED = 'refunded', 'Remboursé'

    reference = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    listing = models.ForeignKey(
        MarketplaceListing,
        on_delete=models.PROTECT,
        related_name='marketplace_orders',
    )
    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='marketplace_orders',
    )
    
    # Montants
    listing_price = models.DecimalField(max_digits=12, decimal_places=2)
    platform_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Statut
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.INITIATED,
    )
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Commande marketplace"
        verbose_name_plural = "Commandes marketplace"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.reference}"
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='marketplace_sales',
    )
    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.INITIATED,
    )
    currency = models.CharField(max_length=10, default='EUR')
    vehicle_price = models.DecimalField(max_digits=10, decimal_places=2)
    marketplace_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    logistics_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    escrow_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    secure_payment_required = models.BooleanField(default=True)
    escrow_required = models.BooleanField(default=True)
    logistics_required = models.BooleanField(default=True)
    shipping_address = models.JSONField(default=dict, blank=True)
    buyer_note = models.TextField(blank=True)
    dispute_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Commande {self.reference} - {self.status}"


class MarketplacePayment(models.Model):
    class Provider(models.TextChoices):
        STRIPE = 'stripe', 'Stripe'
        MOCK = 'mock', 'Mock'
        MANUAL = 'manual', 'Manuel'

    class Status(models.TextChoices):
        CREATED = 'created', 'Cree'
        REQUIRES_ACTION = 'requires_action', 'Action requise'
        PROCESSING = 'processing', 'Traitement'
        SUCCEEDED = 'succeeded', 'Reussi'
        FAILED = 'failed', 'Echoue'
        REFUNDED = 'refunded', 'Rembourse'

    order = models.ForeignKey(
        MarketplaceOrder,
        on_delete=models.CASCADE,
        related_name='payments',
    )
    provider = models.CharField(
        max_length=20,
        choices=Provider.choices,
        default=Provider.MOCK,
    )
    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.CREATED,
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='EUR')
    provider_reference = models.CharField(max_length=255, blank=True)
    client_secret = models.CharField(max_length=255, blank=True)
    provider_payload = models.JSONField(default=dict, blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    refunded_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Paiement {self.order.reference} - {self.status}"


class EscrowAccount(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'En attente'
        FUNDED = 'funded', 'Alimente'
        RELEASED = 'released', 'Libere'
        REFUNDED = 'refunded', 'Rembourse'
        DISPUTED = 'disputed', 'En litige'

    order = models.OneToOneField(
        MarketplaceOrder,
        on_delete=models.CASCADE,
        related_name='escrow',
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    held_amount = models.DecimalField(max_digits=10, decimal_places=2)
    release_token_hash = models.CharField(max_length=128)
    funded_at = models.DateTimeField(null=True, blank=True)
    released_at = models.DateTimeField(null=True, blank=True)
    refunded_at = models.DateTimeField(null=True, blank=True)
    disputed_at = models.DateTimeField(null=True, blank=True)
    dispute_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Escrow {self.order.reference} - {self.status}"

    @classmethod
    def issue_release_token(cls):
        return secrets.token_urlsafe(12)

    def set_release_token(self, token):
        self.release_token_hash = make_password(token)

    def check_release_token(self, token):
        return check_password(token, self.release_token_hash)


class LogisticsShipment(models.Model):
    """Gestion de la logistique et expédition"""
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'En attente'
        SCHEDULED = 'scheduled', 'Planifie'
        PICKED_UP = 'picked_up', 'Recupere'
        IN_TRANSIT = 'in_transit', 'En transit'
        DELIVERED = 'delivered', 'Livre'
        FAILED = 'failed', 'Echec'
        CANCELLED = 'cancelled', 'Annule'

    order = models.OneToOneField(
        MarketplaceOrder,
        on_delete=models.CASCADE,
        related_name='shipment',
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    provider = models.CharField(max_length=100, default='AutoIntel Logistics')
    tracking_number = models.CharField(max_length=100, blank=True)
    pickup_address = models.CharField(max_length=255, blank=True)
    destination_address = models.CharField(max_length=255, blank=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Shipment {self.order.reference} - {self.status}"


class MarketplaceEvent(models.Model):
    order = models.ForeignKey(
        MarketplaceOrder,
        on_delete=models.CASCADE,
        related_name='events',
        null=True,
        blank=True,
    )
    listing = models.ForeignKey(
        MarketplaceListing,
        on_delete=models.CASCADE,
        related_name='events',
        null=True,
        blank=True,
    )
    actor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='marketplace_events',
    )
    event_type = models.CharField(max_length=50)
    payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.event_type} - {self.created_at:%Y-%m-%d %H:%M}"
