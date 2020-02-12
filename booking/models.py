from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils.timezone import now
from django.db.models import Q
# Create your models here.

class BookingExt(models.Manager):

    def createBooking(self,user,flat,days):
        current = self.getCurrentRenta(flat)
        if current is not None:
            return None
        future = self.getFirstFutureRenta(flat)
        date = now()
        if future is not None:
            free_days = abs((date - future.start).days)
            if days > free_days:
                return None
        if days > 100:
            return None 
        return self.create(
                flat = flat,
                rentor = user,
                start = date,
                end = date + timedelta(days=days),
                status = 'pending',
                paid=False,
                created_at = date
            ).setDates().setBookingEnding()

    def getCurrentRenta(self,flat):
        date = now()
        return self.filter(flat=flat,start__lte=date,end__gte=date,status='succeeded',paid=True).last()

    def getDaysBeforeRenta(self,flat):
        future = self.getFirstFutureRenta(flat)
        date = now()
        if future is not None:
            return abs((date - future.start).days)
        return 100

    def getFirstFutureRenta(self,flat):
        date = now()
        return self.filter(flat=flat,start__gte=date,status='succeeded',paid=True).last()

    def getAll(self,flats_queryset):
        '''
        Function returns all flats to map which are not rented yet and booking_ending is not expired
        '''
        date = now()
        b = [i.flat.pk for i in self.filter(~Q(status='canceled'),flat__in=flats_queryset)]
        #,booking_end__gt=date,start__lt=date,paid=False
        print(b)
        flats_queryset = flats_queryset.exclude(id__in=b)
        return flats_queryset

class Booking(models.Model):
    BOOKING_STATS = (
        ('pending', 'Создана'), # Статус сразу после создания аренды
        ('waiting_for_capture', 'Ожидает подтверждения от пользователя'), #Был начат осмотр кв
        ('succeeded', 'Подтверждена \ активна'), # Успешно оплачена
        ('canceled', 'Отменена') # отказ клиентом от аренды
    )
    flat = models.ForeignKey('catalog.Flats', on_delete=models.CASCADE,related_name="Квартира",related_query_name="Квартира")
    rentor = models.ForeignKey(User, models.DO_NOTHING)
    start = models.DateTimeField(verbose_name='Начало аренды',null=True,default=None)
    end = models.DateTimeField(verbose_name='Окончание аренды',null=True,default=None)
    booking_end = models.DateTimeField(null=True,blank=True,verbose_name='Окончание бронироваия',default=None)
    status = models.CharField(max_length=30,null=True,default='pending',choices=BOOKING_STATS)
    paid = models.BooleanField(null=True,default=False)
    created_at = models.DateTimeField(null=True,blank=True,default=None)
    trial_key = models.CharField(max_length=80, blank=True, null=True,default=None)

    extended = BookingExt()
    objects = models.Manager()
    
    def __str__(self):
        return "{0} {1} {2}".format(self.flat,str(self.start),str(self.end))

    class Meta:
        verbose_name = 'Аренда'
        verbose_name_plural = 'Аренды'
        ordering = ['-start']

    def timeIsUp(self):
        '''
            Send signal if booking time is up then do smth
        '''
        if now() > self.booking_end:
            return True
        return False

    def cancel(self):
        if self.status != 'succeeded':
            self.status = 'canceled'
            self.save()
        return self

    def activate(self):
        if self.status != 'succeeded':
            self.status = 'succeeded'
            self.paid = True
            self.save()
        return self
    
    def overviewStart(self):
        if self.status == 'pending':
            self.booking_end = now() + timedelta(minutes=10)
            self.status = 'waiting_for_capture'
            self.save()
        return self

    def getRemainingBookingTime(self):
        return (str(self.booking_end - now())[:7]).replace('days','дней')

    def getRealEnding(self):
        return self.end + timedelta(hours=self.flat.cleaning_time.hour,minutes=self.flat.cleaning_time.minute)

    def setBookingEnding(self):
        '''
        set booking ending time
        '''
        print("setBookingEnding")
        self.booking_end = self.created_at.replace(second=0) + timedelta(hours=self.calcBookingEnding(),seconds=0)
        print(self.booking_end)
        self.save()
        return self
    
    def calcBookingEnding(self):
        '''
        Calc and set booking_end this value depends on created_at
        '''
        cred_at = self.created_at
        if 11 <= cred_at.hour < 15:
            hours = (cred_at.replace(hour=15,minute=0) - cred_at).seconds/3600
            if hours < 2:
                return hours
            return 2
        return 0

    def setDates(self):
        '''
        Set Start to 14h.0m and end to 12h.0m
        '''
        print("setDates")
        self.start = self.start.replace(hour=11,minute=0,second=0)
        self.end = self.end.replace(hour=9,minute=0,second=0)
        print(self.start,self.end)
        self.save()
        return self

    def getDays(self):
        days = ((self.end + timedelta(hours=2))-self.start).days
        if days < 1:
            return 1
        return days

    def getPrice(self):
        return self.getDays() * self.flat.price

    def getDeposit(self):
        return self.flat.deposit