from django import forms
from booking.models import Booking
from django.forms.widgets import SelectDateWidget 
from django.utils import timezone
from datetime import timedelta,datetime
from django.db.models import Q

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

    def clean(self):
        cd = self.cleaned_data
        if str(cd.get('start').time()) != "14:00:00":
            self.add_error('start', "Время не может быть неравно 14:00")

        if str(cd.get('end').time()) != "12:00:00":
            self.add_error('start', "Время не может быть неравно 12:00")

        if cd.get('end') < cd.get('start'):
            self.add_error('end', "Дата окончания аренды не может быть меньше даты начала аренды")