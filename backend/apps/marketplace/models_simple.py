"""
Modèles marketplace simplifiés pour éviter les erreurs
"""

from django.db import models
from django.contrib.auth.models import User


class SellerProfile(models.Model):
    """Profil vendeur simplifié"""
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
    
    def __str__(self):
        return self.company_name or self.user.username


class SimpleListing(models.Model):
    """Annonce simplifiée"""
    
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
        verbose_name = "Annonce simple"
        verbose_name_plural = "Annonces simples"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.brand} {self.model} - {self.year}"


class SimpleOrder(models.Model):
    """Commande simplifiée"""
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'En attente'
        PAID = 'paid', 'Payée'
        SHIPPED = 'shipped', 'Expédiée'
        DELIVERED = 'delivered', 'Livrée'
    
    listing = models.ForeignKey(SimpleListing, on_delete=models.CASCADE, related_name='orders')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='sales')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Commande simple"
        verbose_name_plural = "Commandes simples"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.id}"
