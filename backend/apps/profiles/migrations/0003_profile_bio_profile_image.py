# Generated by Django 5.1.2 on 2024-10-28 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_profile_is_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.FileField(blank=True, default='default/default-user.jpg', null=True, upload_to='image'),
        ),
    ]