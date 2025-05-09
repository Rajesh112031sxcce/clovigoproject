# Generated by Django 5.1.6 on 2025-03-19 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productmodel',
            name='discount_price',
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='product_category',
            field=models.CharField(choices=[('GROCERY', 'Grocery'), ('FOOD', 'Food'), ('DESSERTS', 'Desserts')], max_length=50),
        ),
    ]
