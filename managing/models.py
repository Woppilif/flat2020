from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Partners(models.Model):
    account = models.OneToOneField(User, on_delete=models.CASCADE)
    headmaster = models.CharField(default=None,blank=True,null=True,max_length=60,verbose_name="ФИО")
    hmrank = models.CharField(default=None,blank=True,null=True,max_length=60,verbose_name="Должность")
    org_name = models.CharField(default=None,blank=True,null=True,max_length=60,verbose_name="Название организации")
    document = models.CharField(default=None,blank=True,null=True,max_length=60,verbose_name="Документ, на основнии которого производится работа")
    bitrix_url = models.CharField(default=None,blank=True,null=True,max_length=100,verbose_name="Ссылка фида в Bitrix")
    def __str__(self):
        return str(self.account)

    class Meta:
        verbose_name = 'Партнёр'
        verbose_name_plural = 'Партнёры'

    
    def CheckUserPartner(self):
        return self.account

class Workers(models.Model):
    SHIRT_SIZES = (
        (1, 'Менеджер'),
        (2, 'Клининг'),
        (3, 'Мастер'),
        (4, 'Директор'),
    )
    partner = models.ForeignKey(Partners, on_delete=models.CASCADE)
    account = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.IntegerField(choices=SHIRT_SIZES)
    chat_id = models.IntegerField(default=None,blank=True,null=True)
    def __str__(self):
        return str(self.account)

    class Meta:
        verbose_name = 'Сотрудник партнёра'
        verbose_name_plural = 'Сотрудники партнёров'   

    def CheckUserWorker(self):
        return self.account

def device_status(value):
    print()
    print("This is device_status")
    print(value)

class Devices(models.Model):
    flat = models.ForeignKey('catalog.Flats', on_delete=models.CASCADE,default=None, blank=True, null=True)
    open_key = models.CharField(max_length=60, blank=True, null=True)
    secret_key = models.CharField(max_length=60, blank=True, null=True,default=None)
    app_status = models.BooleanField(blank=True, null=True,default=None)
    created_at = models.DateTimeField(null=True,blank=True,default=None)
    status = models.BooleanField(null=True,default=False,validators=[device_status])
    description = models.CharField(max_length=60, blank=True, null=True,default=None)
    channel_name = models.CharField(max_length=60, blank=True, null=True,default=None)
    class Meta:
        verbose_name = 'Устройство'
        verbose_name_plural = 'Устройства'

    def update(self,status,channel_name=""):
        self.status = status
        self.channel_name = channel_name
        self.save()
        return self

class SystemLogs(models.Model):
    device = models.ForeignKey(Devices, models.DO_NOTHING,blank=True, null=True)
    created_at = models.DateTimeField(null=True,blank=True,auto_created=True)
    comment = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return "{0} - {1}".format(self.comment,self.created_at)
