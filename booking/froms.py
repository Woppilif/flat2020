from django import forms
from booking.models import Booking
from django.core.exceptions import ValidationError

class RentForm(forms.Form):
    def __init__(self,current_flat = None, user = None , *args, **kwargs):
        super(RentForm, self).__init__(*args, **kwargs)
        self.current_flat = current_flat
        self.user = user

    end = forms.IntegerField()

    def clean_end(self):
        end = int(self.cleaned_data['end'])
        print(end)
        if not 1 <= end < Booking.extended.getDaysBeforeRenta(self.current_flat):
            raise  ValidationError("Превышено максимально возможное количество дней.")
        print(end)
        return end

    '''
    def clean(self):
        print(self.cleaned_data)
        end = self.cleaned_data['start'] + timedelta(days=int(self.cleaned_data['end']))
        end = end.replace(hour=12,minute=0)
        r = Rents.objects.filter(
            start__gte=self.cleaned_data['start'].replace(hour=14,minute=0),
            start__lte=end,
            flat=self.current_flat,status=True)
        if r.count():
            self.add_error('start',"Данные даты уже забронированы.")
            raise  ValidationError("Данные даты уже забронированы.")
    '''

    def save(self, commit=True):
        print("ok")
        booking = Booking.extended.createBooking(self.user,self.current_flat,self.cleaned_data['end'])
        booking.createDeal()
        return booking

    class Meta:
        fields = ('end',)
        model = Booking  