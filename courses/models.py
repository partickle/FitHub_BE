from django.db import models

from authorisation.models import CustomUser


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    STATUS_CHOICES = (
        ('completed', 'Completed'),
        ('in progress', 'In progress'),
        ('inactive', 'Inactive'),
    )
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
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='inactive')
    is_pro = models.BooleanField(default=False)
    workouts = models.ManyToManyField('Workout', related_name='courses', blank=True)
    tags = models.ManyToManyField(Tag, related_name='courses')
    hidden = models.BooleanField(default=False)
    owner = models.ForeignKey(CustomUser, related_name='courses', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


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
    image = models.ImageField(upload_to='images/', blank=True, null=True)
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
    image = models.ImageField(upload_to='exercises/images/', blank=True, null=True)
    video = models.FileField(upload_to='exercises/videos/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='inactive')

    def __str__(self):
        return self.name
