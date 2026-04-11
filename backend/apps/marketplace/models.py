"""
Modèles marketplace fonctionnels pour éviter les erreurs
"""

from django.db import models
from django.contrib.auth.models import User


class SellerProfile(models.Model):
    """Profil vendeur fonctionnel"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    company_name = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    description = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    total_sales = models.IntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Profil vendeur"
        verbose_name_plural = "Profils vendeurs"
        db_table = 'marketplace_sellerprofile'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.company_name or self.user.username


class Listing(models.Model):
    """Annonce marketplace fonctionnelle"""
    
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Brouillon'
        PUBLISHED = 'published', 'Publiée'
        SOLD = 'sold', 'Vendue'
    
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=200)
    description = models.TextField()
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Annonce marketplace"
        verbose_name_plural = "Annonces marketplace"
        db_table = 'marketplace_listing'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.brand} {self.model} - {self.year}"


class Transaction(models.Model):
    """Transaction marketplace fonctionnelle"""
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'En attente'
        PAID = 'paid', 'Payée'
        COMPLETED = 'completed', 'Complétée'
    
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='transactions')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='sales')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Transaction marketplace"
        verbose_name_plural = "Transactions marketplace"
        db_table = 'marketplace_transaction'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Transaction {self.id}"


class Review(models.Model):
    """Avis marketplace fonctionnel"""
    
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    reviewed = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='received_reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Avis marketplace"
        verbose_name_plural = "Avis marketplace"
        db_table = 'marketplace_review'
        ordering = ['-created_at']
        unique_together = ['transaction', 'reviewer']
    
    def __str__(self):
        return f"Avis {self.id}"


class Favorite(models.Model):
    """Favoris marketplace fonctionnel"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Favori marketplace"
        verbose_name_plural = "Favoris marketplace"
        db_table = 'marketplace_favorite'
        ordering = ['-created_at']
        unique_together = ['user', 'listing']
    
    def __str__(self):
        return f"Favori {self.id}"


class Message(models.Model):
    """Messages marketplace fonctionnel"""
    
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Message marketplace"
        verbose_name_plural = "Messages marketplace"
        db_table = 'marketplace_message'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message {self.id}"
