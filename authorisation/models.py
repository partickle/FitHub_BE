from django.utils import timezone

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    registration_date = models.DateTimeField(default=timezone.now)


class PremiumSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='premium_subscriptions')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=False)
