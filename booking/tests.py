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


def createBooking(user,flat,days):
    current = Booking.extended.getCurrentRenta(flat)
    if current is not None:
        return None
    future = Booking.extended.getFirstFutureRenta(flat)
    date = now()
    if future is not None:
        free_days = abs((date - future.start).days)
        print(free_days)
        if days > free_days:
            return None
    if days > 100:
        return None 
    return Booking.objects.create(
            flat = flat,
            rentor = user,
            start = date,
            end = date + timedelta(days=days),
            status = True,
            paid=True,
            created_at = date
        ).setDates().setBookingEnding()

user = User.objects.get(pk=1)
flat = Flats.objects.get(pk=125)

print(createBooking(user,flat,3))
'''
flats = Flats.objects.all()

b = Booking.objects.filter(
    flat__in=flats,booking_end__lt=now()
)
b = [i.flat.pk for i in b]
#flats = flats.exclude(b)
flats = flats.exclude(id__in=b)
for i in flats:
    print(i)