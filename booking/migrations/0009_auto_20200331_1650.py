# Generated by Django 3.0.3 on 2020-03-31 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0008_booking_preson_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='preson_amount',
            new_name='person_amount',
        ),
    ]
