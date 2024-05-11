<<<<<<< Updated upstream
=======
import random
import string

from django.db import models
from django.contrib.auth.models import AbstractUser
>>>>>>> Stashed changes
from django.utils import timezone

from django.contrib.auth.models import User
from django.db import models


<<<<<<< Updated upstream
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
=======
class CustomUser(AbstractUser):
>>>>>>> Stashed changes
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    registration_date = models.DateTimeField(default=timezone.now)


<<<<<<< Updated upstream
=======
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')


>>>>>>> Stashed changes
class PremiumSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='premium_subscriptions')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=False)
<<<<<<< Updated upstream
=======

    def is_subscription_active(self):
        return self.is_active and self.start_date <= timezone.now() <= self.end_date


def generate_activation_code():
    digits = string.digits
    return ''.join(random.choice(digits) for _ in range(6))


class ActivationCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    code = models.CharField(max_length=6, default=generate_activation_code)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return (timezone.now() - self.created_at).seconds < 3600

    @classmethod
    def verify_code(cls, user_id, code):
        """
        Проверяет, что введенный код совпадает с сохраненным для пользователя и что он все еще действителен.
        Возвращает True, если код действителен, иначе False.
        """
        try:
            code_obj = cls.objects.get(user_id=user_id, code=code)
            if code_obj.is_valid():
                return True
            return False
        except cls.DoesNotExist:
            return False
>>>>>>> Stashed changes
