from django.test import TestCase
from booking.models import Booking
from django.utils.timezone import now, make_aware, make_naive
from datetime import timedelta
from django.contrib.auth.models import User
# Create your tests here.
from catalog.models import Flats
'''


print(bx.created_at)

b = Booking.extended.getCurrentRenta(
    flat = Flats.objects.get(pk=125)
)

print(b)

flats = Flats.objects.all()

b = Booking.objects.filter(
    flat__in=flats,booking_end__gt=now(),
    start__lt=now()
)
b = [i.flat.pk for i in b]

flats = flats.exclude(id__in=b)
for i in flats:
    print(i)

flats = Flats.objects.all()
b = Booking.extended.getAll(flats)
for i in b:
    print(i)
'''
user = User.objects.get(pk=1)
flat = Flats.objects.get(pk=125)

b = Booking.objects.get(pk=24) #Booking.extended.createBooking(user,flat,1)

print(b)
#b.overviewStart()
print(b.timeIsUp())