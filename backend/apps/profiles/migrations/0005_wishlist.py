# Generated by Django 5.1.2 on 2024-11-04 01:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_sold'),
        ('profiles', '0004_remove_profile_image_profile_profilepic'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlisted_by', to='products.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlisted_users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'product')},
            },
        ),
    ]