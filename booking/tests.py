from django.test import TestCase
from booking.models import Booking
from django.utils import timezone
from datetime import datetime, timedelta
from catalog.models import Flats
from catalog.modules import bitx
from django.utils.timezone import now
from django.db.models import Q
from managing.models import SystemLogs

def check_current_rents():
    status = ""
    flats = bitx.Soap().getAll()
    for i in flats:
        flat, created = Flats.objects.update_or_create(
            internal_id = i.internal_id,
            bxcal_id = i.calendar_id,
        )
        flat.address = i.location['address']
        flat.flat = i.location['flat_number']
        flat.city = i.location['city']
        flat.metro_station = i.location['metro']
        flat.price = i.price
        flat.floor = i.floor
        flat.rooms = i.rooms
        flat.latitude = i.location['latitude']
        flat.longitude = i.location['longitude']
        flat.description = i.description
        flat.status = True
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
                
                r, created = Booking.objects.update_or_create(
                    flat = flat,
                    rentor_id=2,
                    start=start,
                    end=end,
                    paid=True,
                )
                if created:
                    r.status='succeeded'
                    r.save()
                    if r.timeIsUp():
                        r.endRenta()
                
    SystemLogs.objects.create(created_at=now(),comment="Загрузка обновлений из битрикс")
    #logger.info("Checkin renta....")
    return True

check_current_rents()