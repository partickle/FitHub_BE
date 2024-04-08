from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings


# Кастомизированная модель пользователя
class CustomUser(AbstractUser):
    # Дополнительные поля могут быть добавлены сюда
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    registration_date = models.DateTimeField(default=timezone.now)


# Профиль пользователя
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    # Можно добавить дополнительные поля, если это необходимо, но основные уже включены в CustomUser


# Модель премиум подписки
class PremiumSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='premium_subscriptions')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=False)

    def is_subscription_active(self):
        # Этот метод можно использовать для проверки активности подписки
        return self.is_active and self.start_date <= timezone.now() <= self.end_date
