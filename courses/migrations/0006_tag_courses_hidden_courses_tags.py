# Generated by Django 5.0.5 on 2024-05-07 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_courses_exercises_workouts_delete_course_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='courses',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='courses',
            name='tags',
            field=models.ManyToManyField(related_name='courses', to='courses.tag'),
        ),
    ]