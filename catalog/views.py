from django.shortcuts import render, get_object_or_404, redirect
from catalog.models import Flats
from booking.models import Booking
from catalog.modules import pagination
from booking.froms import RentForm
from django.contrib.auth.decorators import login_required
from users.views import sendToBooking, sendToBookingInner, checkcard, checkDocuments
# Create your views here.
@login_required(login_url='/accounts/login/')
@checkDocuments
@sendToBooking
@sendToBookingInner
def map(request):
    flats = Flats.objects.filter(status=True)
    flats = Booking.extended.getAll(flats)
    return render(request, 'catalog/map.html', {"flats":flats})

@login_required(login_url='/accounts/login/')
@checkDocuments
@sendToBooking
@sendToBookingInner
def clist(request,offset=1):
    flats = Flats.objects.filter(status=True)
    flats = Booking.extended.getAll(flats)
    pages = pagination.Pagination(offset,flats,count=5)
    flats = pages.getPaginated()
    return render(request, 'catalog/list.html', {"flats":flats,"pages":pages})
'''
@login_required(login_url='/accounts/login/')
@checkDocuments
@sendToBooking
@sendToBookingInner
'''
def apartment(request,pk=None):
    flat = get_object_or_404(Flats, pk=pk)
    untill = Booking.extended.getDaysBeforeRenta(flat)
    
    if request.method == 'POST':
        if request.user.is_authenticated is False:
            return redirect('login')
        '''
        
        '''
        form = RentForm(data=request.POST, current_flat=flat, user=request.user)
        if form.is_valid():
            renta = form.save()
            return redirect('booking:act',pk=renta.pk)
        else:
            return render(request, 'catalog/apartment.html', {"flat":flat,"untill":untill})
    return render(request, 'catalog/apartment.html', {"flat":flat,"untill":untill})

def index(request):
    if request.user.is_authenticated is True:
        return redirect('catalog:map')
    flats = Flats.objects.filter(status=True)
    flats = Booking.extended.getAll(flats)
    return render(request, 'catalog/index.html', {"flats":flats})

def user_agreement(request):
    return render(request, 'catalog/user_agreement.html',{})

def agreement(request):
    return render(request, 'catalog/agreement.html',{})