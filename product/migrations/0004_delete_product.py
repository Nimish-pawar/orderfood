# Generated by Django 5.0.3 on 2024-06-07 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_cartitem_product'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Product',
        ),
    ]