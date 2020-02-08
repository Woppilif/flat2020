from django.contrib import admin
from managing.models import Devices, Partners, Workers
# Register your models here.
admin.site.register(Partners)
admin.site.register(Workers)
admin.site.register(Devices)
