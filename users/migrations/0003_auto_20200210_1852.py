# Generated by Django 3.0.3 on 2020-02-10 15:52

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200210_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='image_one',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=users.models.get_file_path_users, verbose_name='Фотография первой страницы паспорта'),
        ),
        migrations.AlterField(
            model_name='documents',
            name='image_two',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=users.models.get_file_path_users, verbose_name='Фотография страницы с пропиской'),
        ),
        migrations.AlterField(
            model_name='documents',
            name='ya_card_last4',
            field=models.CharField(blank=True, default=None, max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='documents',
            name='ya_card_type',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='documents',
            name='yakey',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
    ]
