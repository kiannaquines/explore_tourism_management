# Generated by Django 5.1.3 on 2024-12-03 00:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('explore_kabacan_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spot',
            name='spot_img',
        ),
    ]
