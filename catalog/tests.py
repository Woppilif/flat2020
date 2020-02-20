from django.test import TestCase
from catalog.models import Flats
from booking.models import Booking
from managing.models import Partners
from django.contrib.auth.models import User
import requests
from catalog.modules import bitx
from catalog.modules import pagination
from django.utils import timezone
from datetime import datetime, timedelta

from django.utils.timezone import now
from django.db.models import Q
# Create your tests here.
'''
class FlatsTest(TestCase):
    def setUp(self):
        flats = bitx.Soap().getAll()
        for i in flats:
            flat = Flats.objects.create(
                internal_id = i.internal_id,
                bxcal_id = i.calendar_id,
            )
            flat.address = i.location['address']
            flat.flat = i.location['flat_number']
            flat.metro_station = i.location['metro']
            flat.price = i.price
            flat.floor = i.floor
            flat.rooms = i.rooms
            flat.latitude = i.location['latitude']
            flat.longitude = i.location['longitude']
            flat.description = i.description
            flat.save()
            if flat is not None:
                flat.addImages(i.images)
                flat.addItems(i.items)

    def test_flats(self):
        flats = Flats.objects.all()
        for i in flats:
            print(i.getItems())

'''

def pool():
    flats = bitx.Soap().getAll()
    for i in flats:
        flat, created = Flats.objects.update_or_create(
            internal_id = i.internal_id,
            bxcal_id = i.calendar_id,
        )
        flat.address = i.location['address']
        flat.flat = i.location['flat_number']
        flat.metro_station = i.location['metro']
        flat.price = i.price
        flat.floor = i.floor
        flat.rooms = i.rooms
        flat.latitude = i.location['latitude']
        flat.longitude = i.location['longitude']
        flat.description = i.description
        flat.save()
        if flat is not None:
            flat.addImages(i.images)
            flat.addItems(i.items)
            
            for x in i.calendar_ev:
                start = x._begin.replace(hour=14,minute=0)
                end = x._end_time.replace(hour=12,minute=0)

                start = datetime.strptime(str(start)[:16], '%Y-%m-%dT%H:%M')
                end = datetime.strptime(str(end)[:16], '%Y-%m-%dT%H:%M')
            
                start = timezone.make_aware(start)
                end = timezone.make_aware(end)
                r = Booking.objects.update_or_create(
                    flat = flat,
                    rentor_id=2,
                    start=start,
                    end=end,
                    paid=True,
                    status='succeeded'

                )
                print(r)
            

pool()

