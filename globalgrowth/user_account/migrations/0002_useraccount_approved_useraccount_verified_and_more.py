# Generated by Django 5.0.6 on 2024-07-14 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='usertransaction',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='usertransaction',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]