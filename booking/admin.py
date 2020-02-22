from django.contrib import admin
from booking.models import Booking, BookingRate
# Register your models here.

class BookingManager(admin.ModelAdmin):
    #inlines = [ChoiceInline,ChoiceInlineItems]
    list_display = ('flat','rentor','start','end','booking_end','status','paid','timeIsUp')
   
admin.site.register(Booking,BookingManager)
admin.site.register(BookingRate)