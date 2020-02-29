# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from celery.task.schedules import crontab
from celery.decorators import periodic_task

from catalog.modules import bitx
from catalog.models import Flats
from booking.models import Booking
from django.utils import timezone
from datetime import datetime, timedelta

from django.utils.timezone import now
from django.db.models import Q
from managing.models import SystemLogs

logger = get_task_logger(__name__)

@periodic_task(
    run_every=(crontab(minute='*/5')),
    name="check_current",
    ignore_result=True
)
def check_current():
    SystemLogs.objects.create(created_at=now(),comment="Checking rents")
    bookings = Booking.objects.filter(~(Q(status='canceled')|Q(status='ended')),end__lte=now())
    for i in bookings:
        if i.timeIsUp():
            if i.paid:
                i.endRenta()
            else:
                i.cancel()
        else:
            continue
    return True

            


@periodic_task(
    run_every=(crontab(minute='*/15')),
    name="check_current_rents",
    ignore_result=True
)
def check_current_rents():
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
    logger.info("Checkin renta....")
    return True

@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)
