# Generated by Django 5.1.6 on 2025-05-05 05:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_rename_product_category_productmodel_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categorymodel',
            name='parent_category',
        ),
    ]
