# Generated by Django 4.1.2 on 2023-03-30 08:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='recipient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='messages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255, verbose_name='Letter_theme')),
                ('email', models.EmailField(max_length=100, verbose_name='Email')),
                ('content', models.TextField(max_length=500)),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Date_of_create')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='sender_IP')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Feedback',
                'verbose_name_plural': 'Feedback',
                'db_table': 'app_feedback',
                'ordering': ['-time_create'],
            },
        ),
    ]
