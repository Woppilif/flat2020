from django import forms
from booking.models import Booking, BookingRate
from django.core.exceptions import ValidationError

class RentForm(forms.Form):
    def __init__(self,current_flat = None, user = None , *args, **kwargs):
        super(RentForm, self).__init__(*args, **kwargs)
        self.current_flat = current_flat
        self.user = user

    end = forms.IntegerField()

    def clean_end(self):
        end = int(self.cleaned_data['end'])
        if not 1 <= end <= Booking.extended.getDaysBeforeRenta(self.current_flat):
            raise  ValidationError("Превышено максимально возможное количество дней.")
        return end

    
    def clean(self):
        if self.user.documents.status is not True:
            raise  ValidationError("Ваш аккаунт еще не прошёл проверку модератором поэтому Вы не можете забронировать квартиру")   

    def save(self, commit=True):
        booking = Booking.extended.createBooking(self.user,self.current_flat,self.cleaned_data['end'])
        booking.createDeal()
        return booking

    class Meta:
        fields = ('end',)
        model = Booking  

class BookingRateForm(forms.ModelForm):

    cleanness = forms.IntegerField(widget=forms.TextInput(attrs={
        'autocomplete':'off',
        'class':'custom-range',
        'type':'range',
        'min':'1',
        'max':'10',
        'step':'1',
        'value':'8',
        'onChange':'updateCleanness()'
        }),localize=True,label="Чистота помещения 8 из 10")

    staff = forms.IntegerField(widget=forms.TextInput(attrs={
        'autocomplete':'off',
        'class':'custom-range',
        'type':'range',
        'min':'1',
        'max':'10',
        'step':'1',
        'value':'7',
        'onChange':'updateStaff()'
        }),localize=True,label="Оценка работы персонала 7 из 10")

    def clean_cleanness(self):
        cleanness = int(self.cleaned_data['cleanness'])
        if not 1 <= cleanness <= 10:
            raise  ValidationError("Оценка может находиться между 1 и 10!")
        return cleanness  
    
    def clean_staff(self):
        staff = int(self.cleaned_data['staff'])
        if not 1 <= staff <= 10:
            raise  ValidationError("Оценка может находиться между 1 и 10!")
        return staff  

    class Meta:
        fields = ('cleanness','staff',)
        model = BookingRate  