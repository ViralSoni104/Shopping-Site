# Generated by Django 3.0.8 on 2020-10-09 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20201009_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesetting',
            name='About_Us_Image',
            field=models.ImageField(blank=True, upload_to='img/'),
        ),
        migrations.AddField(
            model_name='sitesetting',
            name='About_Us_Image_Alternative_Text',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='sitesetting',
            name='Our_Mission_Image',
            field=models.ImageField(blank=True, upload_to='img/'),
        ),
        migrations.AddField(
            model_name='sitesetting',
            name='Our_Mission_Image_Alternative_Text',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]