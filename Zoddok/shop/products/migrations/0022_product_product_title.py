# Generated by Django 3.1.2 on 2020-12-26 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0021_auto_20201226_1022'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_title',
            field=models.TextField(default=None),
        ),
    ]