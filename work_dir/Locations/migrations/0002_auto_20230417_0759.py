# Generated by Django 3.2.16 on 2023-04-17 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Locations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='time_create',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='time_update',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
