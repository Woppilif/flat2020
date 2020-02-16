from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.models import Documents
from django.core.exceptions import ValidationError
import uuid

class UserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=60,required=True, label='Имя')
    last_name = forms.CharField(max_length=60,required=True, label='Фамилия')
    email = forms.EmailField(required=True, label='Email')
    phone = forms.CharField(max_length=60,required=True, label='Номер телефона')

    class Meta:
        model = User
        fields = ("first_name","last_name","email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Такой email уже зарегистрирован")
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone'].lower()
        r = Documents.objects.filter(phone_number=phone)
        if r.count():
            raise  ValidationError("Такой номер телефона уже зарегистрирован")
        return phone

    def save(self,referal = None, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = user.email
        if commit:
            user.save()
            r = Documents.objects.filter(ref_link=referal).first()
            if r is not None:
                r.bonus = r.bonus + 300
                r.save()

            Documents.objects.create(
                user = user,
                firstname = user.first_name,
                lastname = user.last_name,
                phone_number = self.cleaned_data["phone"],
                ref_link = str(uuid.uuid4()),
                bonus = 300
            )
        return user

class UserDocumentsForm(forms.ModelForm):
    
    def clean_image_one(self):
        image_one = self.cleaned_data['image_one']
        print(image_one)
        if image_one is None:
            raise  ValidationError("Данное поле обязательно для заполнения")
        return image_one

    def clean_image_two(self):
        image_two = self.cleaned_data['image_two']
        if image_two is None:
            raise  ValidationError("Данное поле обязательно для заполнения")
        return image_two


    class Meta:
        fields = ('image_one','image_two',)
        model = Documents