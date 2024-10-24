# Generated by Django 5.1.2 on 2024-10-23 23:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('category', models.CharField(choices=[('Textbook', 'Textbook'), ('Clothing', 'Clothing'), ('Furniture', 'Furniture'), ('Electronics', 'Electronics'), ('Stationary', 'Stationary'), ('Miscellaneous', 'Miscellaneous')], max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('condition', models.CharField(choices=[('New', 'New'), ('Like New', 'Used - Like New'), ('Good', 'Used - Good'), ('Fair', 'Used - Fair')], max_length=255)),
                ('pickup_location', models.CharField(choices=[('Robarts', 'Robarts'), ('Gerstein', 'Gerstein'), ('Computer Science Library', 'Computer Science Library'), ('Bahen', 'Bahen'), ('Galbraith', 'Galbraith'), ('Sanford Fleming', 'Sanford Fleming')], max_length=255)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('edited_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
