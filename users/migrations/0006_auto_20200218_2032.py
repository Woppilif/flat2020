# Generated by Django 3.0.3 on 2020-02-18 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200218_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='status',
            field=models.BooleanField(choices=[(None, 'Создан'), (False, 'Не подтвержден'), (True, 'Подтверждён')], default=None, null=True),
        ),
    ]
