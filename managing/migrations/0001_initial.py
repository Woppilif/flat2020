# Generated by Django 3.0 on 2020-02-04 11:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import managing.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalog', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Partners',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headmaster', models.CharField(blank=True, default=None, max_length=60, null=True, verbose_name='ФИО')),
                ('hmrank', models.CharField(blank=True, default=None, max_length=60, null=True, verbose_name='Должность')),
                ('org_name', models.CharField(blank=True, default=None, max_length=60, null=True, verbose_name='Название организации')),
                ('document', models.CharField(blank=True, default=None, max_length=60, null=True, verbose_name='Документ, на основнии которого производится работа')),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Партнёр',
                'verbose_name_plural': 'Партнёры',
            },
        ),
        migrations.CreateModel(
            name='Workers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.IntegerField(choices=[(1, 'Менеджер'), (2, 'Клининг'), (3, 'Мастер')])),
                ('chat_id', models.IntegerField(blank=True, default=None, null=True)),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='managing.Partners')),
            ],
            options={
                'verbose_name': 'Сотрудник партнёра',
                'verbose_name_plural': 'Сотрудники партнёров',
            },
        ),
        migrations.CreateModel(
            name='Devices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open_key', models.CharField(blank=True, max_length=60, null=True)),
                ('secret_key', models.CharField(blank=True, default=None, max_length=60, null=True)),
                ('app_status', models.BooleanField(blank=True, default=None, null=True)),
                ('created_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('status', models.BooleanField(default=False, null=True, validators=[managing.models.device_status])),
                ('description', models.CharField(blank=True, default=None, max_length=60, null=True)),
                ('flat', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.Flats')),
            ],
            options={
                'verbose_name': 'Устройство',
                'verbose_name_plural': 'Устройства',
            },
        ),
    ]
