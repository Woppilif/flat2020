from django.db import models
from django.contrib.auth.models import User
import uuid
import os
# Create your models here.

def get_file_path_users(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('users/images', filename)

class Documents(models.Model):
    STATUS_TYPES = (
        (False, 'Не подтвержден'),
        (True, 'Подтверждён')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50,default="", blank=False, null=False,verbose_name="Имя")
    lastname = models.CharField(max_length=50,default="", blank=False, null=False,verbose_name="Фамилия")
    phone_number = models.CharField(max_length=50,default="", blank=False, null=False,verbose_name="Телефонный номер")
    image_one = models.ImageField(upload_to=get_file_path_users,default=None,verbose_name="Фотография первой страницы паспорта", blank=True, null=True)
    image_two = models.ImageField(upload_to=get_file_path_users,default=None,verbose_name="Фотография страницы с пропиской", blank=True, null=True)
    status = models.BooleanField(null=False,default=False,choices=STATUS_TYPES)
    yakey = models.CharField(max_length=50,default=None, blank=True, null=True)
    ya_card_type = models.CharField(max_length=50,default=None, blank=True, null=True)
    ya_card_last4 = models.CharField(max_length=4,default=None, blank=True, null=True)
    totlal_cancelation = models.IntegerField(null=True,default=0,blank=True)    
    bonus = models.IntegerField(default=0,blank=True,null=True)
    ref_link = models.CharField(max_length=50,default=None, blank=True, null=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Документы пользователей'
        verbose_name_plural = 'Документы пользователей'

    def get_absolute_url(self):
        from django.urls import reverse
        return "{0}?ref={1}".format(reverse('users:registration'),self.ref_link) 

    def addCard(self,payment):
        self.yakey = payment.payment_method.id
        self.ya_card_type = payment.payment_method.card.card_type
        self.ya_card_last4 = payment.payment_method.card.last4
        self.save()

    def deleteCard(self):
        self.yakey = None
        self.ya_card_type = None
        self.ya_card_last4 = None
        self.save()
    
class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flat = models.ForeignKey('catalog.Flats', on_delete=models.CASCADE,blank=True, null=True)
    class Meta:
        verbose_name = 'Закладка пользователя'
        verbose_name_plural = 'Закладки пользователей'