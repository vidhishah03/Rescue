# Generated by Django 3.1.1 on 2021-03-24 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_profile_about_me'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
