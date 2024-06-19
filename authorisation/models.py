from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from FitHub_BE import settings
from courses.models import UserCourse


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
    photo = models.ImageField(upload_to='media/profile_photos/', null=True, blank=True)
    registration_date = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def get_active_courses(self):
        return self.user_courses.filter(status='in_progress')

    def start_course(self, course):
        user_course, created = UserCourse.objects.get_or_create(
            user=self, course=course, defaults={'status': 'in_progress', 'start_date': timezone.now()}
        )
        if not created:
            user_course.status = 'in_progress'
            user_course.start_date = timezone.now()
            user_course.save()
        return user_course

    def complete_course(self, course):
        try:
            user_course = UserCourse.objects.get(user=self, course=course)
            user_course.status = 'completed'
            user_course.end_date = timezone.now()
            user_course.save()
        except UserCourse.DoesNotExist:
            raise ValueError("Пользователь не начинал этот курс")


class PremiumSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='premium_subscriptions')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=False)

    def is_subscription_active(self):
        return self.is_active and self.start_date <= timezone.now() <= self.end_date
