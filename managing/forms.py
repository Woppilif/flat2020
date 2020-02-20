from django import forms
from booking.models import Booking
from django.forms.widgets import SelectDateWidget 
from django.utils import timezone
from datetime import timedelta,datetime,date
from django.db.models import Q
import uuid
from django.core.exceptions import ValidationError

class RentFormEx(forms.ModelForm):

    paid = forms.ChoiceField(choices=(
        (True,'Оплачена наличными'),
        (False, 'Оплата картой клиента')
    ),label="Кем будет производиться оплата")
    
    start = forms.DateField(widget=SelectDateWidget(empty_label="Nothing"),initial=timezone.now(),label="Начало аренды")
    end = forms.DateField(widget=SelectDateWidget(empty_label="Nothing"),initial=timezone.now() + timedelta(days=1),label="Окончание аренды")
        
  
    class Meta:
        fields = ('flat','start','end','paid')
        model = Booking

    def clean_start(self):
        start = self.cleaned_data['start']
        if start < date.today():
            raise  ValidationError("Дата начала аренды не может быть позднее, чем сегодня")
        return datetime.combine(start, datetime.min.time())

    def clean_end(self):
        end = self.cleaned_data['end']
        if end < date.today():
            raise  ValidationError("Дата окончания аренды не может быть позднее, чем сегодня")
        return datetime.combine(end, datetime.min.time())

    def save(self, commit=True):
        status = None
        paid = None
        if self.cleaned_data['paid'] == "False":
            status = 'waiting_for_capture'
            paid = False
        elif self.cleaned_data['paid'] == "True":
            status = 'succeeded'
            paid = True
        else:
            return False
        
        booking = Booking.objects.create(
            flat=self.cleaned_data['flat'],
            rentor_id=2,
            start=datetime.combine(self.cleaned_data['start'], datetime.min.time()),
            end=datetime.combine(self.cleaned_data['end'], datetime.min.time()),
            paid=paid,
            status=status,
            trial_key=str(uuid.uuid4())

        ).setDates(add=3)
        print(booking)
        '''
        booking.createDeal()
        '''
        return True