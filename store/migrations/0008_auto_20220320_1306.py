# Generated by Django 3.1.14 on 2022-03-20 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_product_brand'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='email',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='name',
        ),
    ]
