from django.test import TestCase
from catalog.models import Flats
from managing.models import Partners
from django.contrib.auth.models import User
import requests
from catalog.modules import bitx

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

pool()