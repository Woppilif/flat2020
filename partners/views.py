from django.shortcuts import render, get_object_or_404, redirect
from managing.models import Partners
from partners.forms import OrganizationForm
# Create your views here.

def index(request):
    organization = Partners.objects.get(account=request.user)
    if request.method == 'POST':
        form = OrganizationForm(data=request.POST,instance=organization)
        if form.is_valid():
            form.save()
        return redirect('partners:index')
    form = OrganizationForm(instance=organization)
    return render(request,"partners/main/index.html",{"form":form})

