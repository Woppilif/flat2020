# Generated by Django 3.0.3 on 2020-02-10 15:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phone_field.models
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0005_auto_20200209_1847'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.Flats')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Закладка пользователя',
                'verbose_name_plural': 'Закладки пользователей',
            },
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(default='', max_length=50, verbose_name='Имя')),
                ('lastname', models.CharField(default='', max_length=50, verbose_name='Фамилия')),
                ('phone_number', phone_field.models.PhoneField(blank=True, help_text='Contact phone number', max_length=31)),
                ('image_one', models.ImageField(default=None, upload_to=users.models.get_file_path_users, verbose_name='Фотография первой страницы паспорта')),
                ('image_two', models.ImageField(default=None, upload_to=users.models.get_file_path_users, verbose_name='Фотография страницы с пропиской')),
                ('status', models.BooleanField(choices=[(False, 'Не подтвержден'), (True, 'Подтверждён')], default=False)),
                ('yakey', models.CharField(default=None, max_length=50, null=True)),
                ('ya_card_type', models.CharField(default=None, max_length=50, null=True)),
                ('ya_card_last4', models.CharField(default=None, max_length=4, null=True)),
                ('totlal_cancelation', models.IntegerField(blank=True, default=0, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Документы пользователей',
                'verbose_name_plural': 'Документы пользователей',
            },
        ),
    ]
