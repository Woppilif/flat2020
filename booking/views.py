from django.shortcuts import render, get_object_or_404, redirect
from booking.models import Booking
from django.db.models import Q
from payments.models import Transactions
from django.contrib.auth.decorators import login_required
from users.views import sendToBooking, sendToBookingInner, checkcard, checkDocuments
# Create your views here.
@login_required(login_url='/accounts/login/')
@checkDocuments
@checkcard
@sendToBookingInner
def index(request,pk):
    renta = get_object_or_404(Booking,Q(status="pending") | Q(status="waiting_for_capture"), pk=pk,rentor=request.user,paid=False)
    if request.method == 'POST':
        if "pay" in request.POST:
            t =  Transactions.yandex.createPayment(
                request.user,
                renta.getPrice(),
                renta,
                payment_type=True
            )
            transaction = Transactions.objects.get(payment_id=t.id)
            transaction.capture()
            transaction.setInfo(transaction.getInfo())
            transaction.checkout()
            print(transaction.status)
            return redirect('booking:opendoor',pk=renta.pk)
        if "cancel" in request.POST:
            renta.cancel()
            return redirect('catalog:map')
        if "open" in request.POST:
            renta.overviewStart()
            if not renta.timeIsUp():
                print("send signal")
            else:
                print("time is up do smth")
            return redirect('booking:act',pk=renta.pk)
    return render(request, 'booking/act.html', {"renta":renta})

@login_required(login_url='/accounts/login/')
@checkDocuments
@sendToBooking
def opendoor(request,pk):
    renta = get_object_or_404(Booking,status='succeeded', pk=pk,rentor=request.user,paid=True)
    if request.method == 'POST':
        if "open" in request.POST:
            if not renta.timeIsUp():
                print("send signal")
            else:
                print("time is up do smth")
            return redirect('booking:opendoor',pk=renta.pk)
        if "end" in request.POST:
            renta.deactivate()
            return redirect('catalog:map')
    return render(request, 'booking/opendoor.html', {"renta":renta})