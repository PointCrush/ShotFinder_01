# Generated by Django 3.2.16 on 2023-04-18 08:12

import Studios.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Studio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255)),
                ('telephone_number', models.CharField(max_length=100)),
                ('mail', models.CharField(max_length=100)),
                ('logo', models.ImageField(upload_to='studio_logo_directory_path')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('schedule', models.TextField()),
                ('way', models.TextField()),
                ('price', models.TextField()),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('time_update', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudioImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=Studios.models.studio_directory_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('studio', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='Studios.studio')),
            ],
        ),
    ]