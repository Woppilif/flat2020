from django.db import models
#from managing.models import Partners
# Create your models here.
class Flats(models.Model):
    FLAT_STATS = (
        (False, 'Не показывается в каталоге'),
        (True, 'Показывается в каталоге')
    )
    partner = models.ForeignKey('managing.Partners', on_delete=models.CASCADE, blank=True, null=True)
    status = models.BooleanField(blank=True, null=True,choices=FLAT_STATS)
    city = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=80, blank=True, null=True)
    flat = models.CharField(max_length=80, blank=True, null=True)
    floor = models.IntegerField(blank=True, null=True)
    rooms = models.IntegerField(blank=True, null=True,default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    deposit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    hint = models.CharField(max_length=50, blank=True, null=True)
    cleaning_time = models.TimeField(blank=True, null=True,default="3:00")
    metro_station = models.CharField(max_length=60, blank=True, null=True)
    bxcal_id = models.IntegerField(blank=True, null=True,default=None)
    internal_id = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квартиры'

    def addImages(self,images_list = []):
        for i in images_list:
            Images.objects.create(flat=self,img_url=i,urled=True)
        return True

    def addItems(self, items_list = []):
        for i in items_list:
            FlatsItems.objects.create(falt_id=self.pk,item_name=i[0],item_count=i[1])
        return True

    def flatsItems(self):
        return FlatsItems.objects.filter(flat=self)

    def getImages(self):
        return Images.objects.filter(flat=self)
    
    def getPreview(self):
        return Images.objects.filter(flat=self).first()

class FlatsItems(models.Model):
    flat = models.ForeignKey(Flats, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=50, blank=True, null=True,verbose_name="Предмет (Стол, стул)")
    item_count = models.IntegerField(blank=True,null=True,default=0,verbose_name="Количество предметов (целое число)")
    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def __str__(self):
        return "{0} {1} шт.".format(self.item_name,self.item_count)

class Images(models.Model):
    flat = models.ForeignKey(Flats, on_delete=models.CASCADE)
    images = models.CharField(max_length=255,blank=True, null=True,default=None)
    img_url = models.CharField(max_length=255,blank=True, null=True,default=None)
    urled = models.BooleanField(blank=True, null=True,default=False)

    def __str__(self):
        return "{0} {1}".format(self.flat,self.pk)
    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

