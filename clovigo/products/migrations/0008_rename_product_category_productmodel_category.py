# Generated by Django 5.1.6 on 2025-05-05 05:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_productmodel_product_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productmodel',
            old_name='product_category',
            new_name='category',
        ),
    ]
