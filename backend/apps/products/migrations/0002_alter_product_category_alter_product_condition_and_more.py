# Generated by Django 4.2.16 on 2024-10-25 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('1', 'Category 1'), ('2', 'Category 2'), ('3', 'Category 3'), ('4', 'Category 4')], max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='condition',
            field=models.CharField(choices=[('1', 'New'), ('2', 'Used - Like New'), ('3', 'Used - Good'), ('4', 'Used - Fair')], max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='pickup_location',
            field=models.CharField(choices=[('1', 'Robarts'), ('2', 'Gerstein'), ('3', 'Computer Science Library'), ('4', 'Bahen'), ('5', 'Galbraith'), ('6', 'Sanford Fleming'), ('7', 'Bahen')], max_length=255),
        ),
    ]
