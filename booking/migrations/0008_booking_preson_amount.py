# Generated by Django 3.0.3 on 2020-03-31 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0007_auto_20200222_2211'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='preson_amount',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Количество человек'),
        ),
    ]
