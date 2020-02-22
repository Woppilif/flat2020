from django.contrib import admin
from booking.models import Booking
# Register your models here.

class BookingManager(admin.ModelAdmin):
    #inlines = [ChoiceInline,ChoiceInlineItems]
    list_display = ('flat','rentor','start','end','booking_end','status','paid','timeIsUp')
   
admin.site.register(Booking,BookingManager)