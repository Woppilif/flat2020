from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils.timezone import now
# Create your models here.

class BookingExt(models.Manager):

    def getCurrentRenta(self,flat):
        date = now()
        return self.filter(flat=flat,start__lte=date,end__gte=date,status=True,paid=True).last()

    def getFirstFutureRenta(self,flat):#
        date = now()
        return self.filter(flat=flat,start__gte=date,status=True,paid=True).last()

    def getAll(self,flats_queryset):
        '''
        Function returns all flats to map
        '''
        date = now()
        return self.filter(flat__in=flats_queryset,booking_end__gt=date)

class Booking(models.Model):
    flat = models.ForeignKey('catalog.Flats', on_delete=models.CASCADE,related_name="Квартира",related_query_name="Квартира")
    rentor = models.ForeignKey(User, models.DO_NOTHING)
    start = models.DateTimeField(verbose_name='Начало аренды',null=True,default=None)
    end = models.DateTimeField(verbose_name='Окончание аренды',null=True,default=None)
    booking_end = models.DateTimeField(null=True,blank=True,verbose_name='Окончание бронироваия',default=None)
    status = models.BooleanField(null=True,default=False)
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

    def getRealEnding(self):
        return self.end + timedelta(hours=self.flat.cleaning_time.hour,minutes=self.flat.cleaning_time.minute)

    def setBookingEnding(self):
        '''
        set booking ending time
        '''
        print("setBookingEnding")
        self.booking_end = self.created_at + timedelta(hours=self.calcBookingEnding())
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