from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [
    ]
    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('duration', models.IntegerField(help_text='Total duration in days')),
                ('category', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('video', models.FileField(blank=True, null=True, upload_to='videos/')),
                ('status', models.CharField(
                    choices=[('completed', 'Completed'), ('in progres', 'In progres'), ('inactive', 'Inactive')],
                    default='Inactive', max_length=20)),
            ],
        ),
    ]
