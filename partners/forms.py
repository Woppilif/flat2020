from django import forms
from managing.models import Partners

class OrganizationForm(forms.ModelForm):
    headmaster = forms.CharField(label="ФИО Директора")
    hmrank = forms.CharField(label="Должность")
    org_name = forms.CharField(label="Наименование организации")
    document = forms.CharField(label="Документ, на основании которого осуществляется деятельность")
    #bitrix_url = forms.CharField()

    class Meta:
        fields = ('headmaster','hmrank','org_name','document')
        model = Partners