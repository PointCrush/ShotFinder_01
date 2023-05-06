# Generated by Django 3.2.16 on 2023-04-18 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Studios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studio',
            name='logo',
            field=models.ImageField(null=True, upload_to='studio_logo_directory_path'),
        ),
        migrations.AlterField(
            model_name='studio',
            name='mail',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='studio',
            name='price',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='studio',
            name='schedule',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='studio',
            name='telephone_number',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='studio',
            name='way',
            field=models.TextField(null=True),
        ),
    ]
