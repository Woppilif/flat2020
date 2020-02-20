from django.shortcuts import render, get_object_or_404, redirect
from booking.models import Booking
from django.db.models import Q
from payments.models import Transactions
from django.contrib.auth.decorators import login_required
from users.views import sendToBooking, sendToBookingInner, checkcard, checkDocuments
from managing.views import openDoorAPI
from managing.models import Devices
# Create your views here.
@login_required(login_url='/accounts/login/')
@checkDocuments
@checkcard
@sendToBookingInner
def index(request,pk):
    renta = get_object_or_404(Booking,Q(status="pending") | Q(status="waiting_for_capture"), pk=pk,rentor=request.user,paid=False)
    device = get_object_or_404(Devices,flat=renta.flat)
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
            renta.cancelDeal()
            return redirect('catalog:map')
        if "open" in request.POST:
            renta.overviewStart()
            if not renta.timeIsUp():
                print("send signal")
                openDoorAPI(device.id,'open',device.secret_key)
            else:
                print("time is up do smth")
            return redirect('booking:act',pk=renta.pk)
    return render(request, 'booking/act.html', {"renta":renta})

@login_required(login_url='/accounts/login/')
@checkDocuments
@sendToBooking
def opendoor(request,pk):
    renta = get_object_or_404(Booking,status='succeeded', pk=pk,rentor=request.user,paid=True)
    device = get_object_or_404(Devices,flat=renta.flat)
    if request.method == 'POST':
        if "open" in request.POST:
            if not renta.timeIsUp():
                print("send signal")
                openDoorAPI(device.id,'open',device.secret_key)
            else:
                print("time is up do smth")
            return redirect('booking:opendoor',pk=renta.pk)
        if "end" in request.POST:
            renta.deactivate()
            return redirect('catalog:map')
    return render(request, 'booking/opendoor.html', {"renta":renta})

def trial_booking(request,trial_key):
    renta = get_object_or_404(Booking,trial_key=trial_key)
    device = get_object_or_404(Devices,flat=renta.flat)
    if renta.paid is False:
        return redirect("payments:booking",trial_key=trial_key)
    if request.method == 'POST':
        if "open" in request.POST:
            if not renta.timeIsUp():
                print("send signal")
                openDoorAPI(device.id,'open',device.secret_key)
            else:
                print("time is up do smth")
            return redirect('booking:trial',trial_key=trial_key)
        if "end" in request.POST:
            renta.deactivate()
            return redirect('catalog:map')
    return render(request, 'booking/opendoor.html', {"renta":renta})