# Generated by Django 3.0.3 on 2020-02-22 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_auto_20200218_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='payment_type',
            field=models.CharField(blank=True, choices=[('account', 'Привязка карты'), ('deposit', 'Депозит'), ('full', 'Полная стоимость'), ('usercard', 'Оплата картой клиента'), ('trial', 'Оплата аренды без регистрации')], default='account', max_length=40, null=True),
        ),
    ]
