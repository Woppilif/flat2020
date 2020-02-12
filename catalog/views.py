from django.shortcuts import render, get_object_or_404, redirect
from catalog.models import Flats
from booking.models import Booking
from catalog.modules import pagination
from booking.froms import RentForm
# Create your views here.
def index(request):
    flats = Flats.objects.filter(status=True)
    flats = Booking.extended.getAll(flats)
    return render(request, 'catalog/map.html', {"flats":flats})

def clist(request,offset=1):
    flats = Flats.objects.filter(status=True)
    flats = Booking.extended.getAll(flats)
    pages = pagination.Pagination(offset,flats,count=5)
    flats = pages.getPaginated()
    return render(request, 'catalog/list.html', {"flats":flats,"pages":pages})

def apartment(request,pk=None):
    flat = get_object_or_404(Flats, pk=pk)
    untill = Booking.extended.getDaysBeforeRenta(flat)
    if request.method == 'POST':
        print("here")
        form = RentForm(data=request.POST, current_flat=flat, user=request.user)
        if form.is_valid():
            renta = form.save()
            return redirect('booking:act',pk=renta.pk)
        else:
            return render(request, 'catalog/apartment.html', {"flat":flat,"untill":untill})
    return render(request, 'catalog/apartment.html', {"flat":flat,"untill":untill})