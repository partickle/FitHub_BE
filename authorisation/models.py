import random
import string

from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from FitHub_BE import settings


class UserProfile(models.Model):
    GOAL_CHOICES = [
        ('gain_weight', 'Gain weight'),
        ('lose_weight', 'Lose weight'),
        ('get_fitter', 'Get fitter'),
        ('gain_flexibility', 'Gain more flexible'),
        ('learn_the_basic', 'Learn the basic'),
    ]

    ACTIVITY_LEVEL_CHOICES = [
        ('rookie', 'Rookie'),
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advance'),
        ('true_beast', 'True beast'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile', null=True, blank=True)
    is_male = models.BooleanField(default=True)
    age = models.PositiveIntegerField()
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES)
    physical_activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL_CHOICES)


class WorkoutSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='workout_sessions')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def duration(self):
        return self.end_time - self.start_time

    @classmethod
    def total_workout_time(cls, user, date):
        sessions = cls.objects.filter(user=user, start_time__date=date)
        total_time = sum((session.duration() for session in sessions), timezone.timedelta())
        return total_time


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    registration_date = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class PremiumSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='premium_subscriptions')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=False)

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
