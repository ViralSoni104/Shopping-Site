# Generated by Django 3.0.8 on 2020-10-09 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20201009_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesetting',
            name='about_page_meta_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sitesetting',
            name='about_page_meta_keywords',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sitesetting',
            name='contact_page_meta_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sitesetting',
            name='contact_page_meta_keywords',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sitesetting',
            name='home_page_meta_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sitesetting',
            name='home_page_meta_keywords',
            field=models.TextField(blank=True, null=True),
        ),
    ]