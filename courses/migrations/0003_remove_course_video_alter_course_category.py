from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('courses', '0002_course_is_pro'),
    ]
    operations = [
        migrations.RemoveField(
            model_name='course',
            name='video',
        ),
        migrations.AlterField(
            model_name='course',
            name='category',
            field=models.CharField(
                choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advance', 'Advance')],
                default='beginner', max_length=20),
        ),
    ]
