# Generated by Django 5.1.1 on 2024-09-24 21:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_agents', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='withdrawalrequest',
            name='payment_agent',
        ),
        migrations.AlterField(
            model_name='withdrawalrequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='withdrawal_requests', to=settings.AUTH_USER_MODEL),
        ),
    ]
