# Generated by Django 3.1.1 on 2021-03-24 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_profile_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='https://artyaunt.com/wp-content/uploads/2019/09/member-default.jpg', upload_to='profile_pics'),
        ),
    ]
