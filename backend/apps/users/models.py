from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.core.models import TimeStampedModel

class UserProfile(TimeStampedModel):
    COUNTRY_CHOICES = [
        ('DZ', 'Algérie'), ('TN', 'Tunisie'),
        ('FR', 'France'), ('MA', 'Maroc')
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile'
    )
    country = models.CharField(
        max_length=5, default='DZ', choices=COUNTRY_CHOICES
    )
    phone = models.CharField(max_length=20, blank=True)
    telegram_chat_id = models.CharField(max_length=100, blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True)

    # Compteurs
    estimations_this_month = models.IntegerField(default=0)
    total_estimations = models.IntegerField(default=0)
    last_active = models.DateTimeField(null=True, blank=True)

    # Gamification
    xp = models.IntegerField(default=0)
    level = models.SmallIntegerField(default=1)
    coins = models.IntegerField(default=100)
    xp_pct = models.SmallIntegerField(default=0)

    XP_THRESHOLDS = [0, 500, 1500, 3500, 7000, 12000, 20000]
    LEVEL_NAMES = [
        'Apprenti Mécanicien', 'Conducteur Éclairé',
        'Expert Automobile', 'Maître du Marché',
        'Analyste Légendaire', 'Oracle AutoIntel',
    ]

    def add_xp(self, amount):
        self.xp += amount
        while (self.level < len(self.XP_THRESHOLDS) - 1 and
               self.xp >= self.XP_THRESHOLDS[self.level]):
            self.level += 1
        current_threshold = self.XP_THRESHOLDS[self.level - 1]
        next_threshold = self.XP_THRESHOLDS[min(
            self.level, len(self.XP_THRESHOLDS) - 1)]
        if next_threshold > current_threshold:
            self.xp_pct = int(
                (self.xp - current_threshold)
                / (next_threshold - current_threshold) * 100
            )
        self.save(update_fields=['xp', 'level', 'xp_pct'])

    def add_coins(self, amount):
        self.coins = max(0, self.coins + amount)
        self.save(update_fields=['coins'])

    @property
    def level_name(self):
        idx = min(self.level - 1, len(self.LEVEL_NAMES) - 1)
        return self.LEVEL_NAMES[idx]

    @property
    def plan(self):
        try:
            return self.user.subscription.plan.name
        except:
            return 'free'

    @property
    def can_estimate(self):
        limits = {'free': 10, 'pro': 999999, 'business': 999999}
        return self.estimations_this_month < limits.get(self.plan, 10)

    def __str__(self):
        return f"Profile({self.user.username})"


