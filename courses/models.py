from django.db import models
from django.db.models import Avg
from django.utils.timezone import now, timedelta
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class CourseQuerySet(models.QuerySet):
    def recent(self):
        recent_threshold = timezone.now() - timedelta(days=30)
        return self.filter(created_at__gte=recent_threshold)

    def critical(self):
        return self.filter(ratings__rating__lt=2)

    def favourable(self):
        return self.filter(ratings__rating__gte=4)

class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField(help_text="Total duration in days")
    category = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    image = models.ImageField(upload_to='media/images/courses', blank=True, null=True)
    is_pro = models.BooleanField(default=False)
    workouts = models.ManyToManyField('Workout', related_name='courses', blank=True)
    tags = models.ManyToManyField(Tag, related_name='courses')
    hidden = models.BooleanField(default=False)
    owner = models.ForeignKey('authorisation.CustomUser', related_name='courses', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = CourseQuerySet.as_manager()

    def __str__(self):
        return self.name
    
    def average_rating(self):
        avg_rating = self.ratings.aggregate(Avg('rating'))['rating__avg']
        return avg_rating if avg_rating is not None else 0.0


class CourseRating(models.Model):
    course = models.ForeignKey(Course, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey('authorisation.CustomUser', related_name='course_ratings', on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating} by {self.user} for {self.course}"


class Workout(models.Model):
    STATUS_CHOICES = (
        ('completed', 'Completed'),
        ('in progress', 'In progress'),
        ('inactive', 'Inactive'),
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in minutes")
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/images/workouts', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='inactive')
    exercises = models.ManyToManyField('Exercise', related_name='workouts')

    def __str__(self):
        return self.name

class Exercise(models.Model):
    STATUS_CHOICES = (
        ('completed', 'Completed'),
        ('in progress', 'In progress'),
        ('inactive', 'Inactive'),
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in seconds")
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/images/exercises', blank=True, null=True)
    video = models.FileField(upload_to='media/videos/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='inactive')

    def __str__(self):
        return self.name

class UserCourse(models.Model):
    STATUS_CHOICES = (
        ('completed', 'Завершен'),
        ('in_progress', 'В процессе'),
        ('inactive', 'Неактивен'),
    )

    user = models.ForeignKey('authorisation.CustomUser', on_delete=models.CASCADE, related_name='user_courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='user_courses')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='inactive')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.email} - {self.course.name} - {self.status}"
