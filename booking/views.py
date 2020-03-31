from django.shortcuts import render, get_object_or_404, redirect
from booking.models import Booking, BookingRate
from django.db.models import Q
from payments.models import Transactions
from django.contrib.auth.decorators import login_required
from users.views import sendToBooking, sendToBookingInner, checkcard, checkDocuments
from managing.views import openDoorAPI
from managing.models import Devices, SystemLogs
from booking.froms import BookingRateForm
from django.utils.timezone import now
import uuid
# Create your views here.
@login_required(login_url='/accounts/login/')
@checkDocuments
@checkcard
@sendToBookingInner
def index(request,pk):
    renta = get_object_or_404(Booking,Q(status="pending") | Q(status="waiting_for_capture"), pk=pk,rentor=request.user,paid=False)
    device = Devices.objects.filter(flat=renta.flat).first()
    if request.method == 'POST':
        if "pay" in request.POST:
            if request.user.documents.yakey == "" or request.user.documents.yakey is None:
                return redirect("payments:index")
            t =  Transactions.yandex.createPayment(
                request.user,
                renta.getPrice(),
                renta,
                payment_type='full'
            )
            transaction = Transactions.objects.get(payment_id=t.id)
            transaction.capture()
            transaction.setInfo(transaction.getInfo())
            transaction.checkout()
            print(transaction.status)
            return redirect('booking:opendoor',pk=renta.pk)
        if "tinkoff" in request.POST:
            renta.status = "waiting_for_capture"
            renta.trial_key = str(uuid.uuid4())
            renta.save()
            return redirect("https://www.tinkoff.ru/rm/gayfutdinov.ilsur1/P7Dhg60333/")
        if "cancel" in request.POST:
            renta.cancel()
            renta.cancelDeal()
            return redirect('catalog:map')
        if "open" in request.POST:
            SystemLogs.objects.create(device=device,comment="Нажали кнопку открыть дверь. Статус аренды: {0}".format(renta.timeIsUp()))
            renta.overviewStart()
            if not renta.timeIsUp():
                print("send signal")
                openDoorAPI(device.channel_name,'open',device.secret_key)
            else:
                print("time is up do smth")
            return redirect('booking:act',pk=renta.pk)
    return render(request, 'booking/act.html', {"renta":renta,"device":device,"date":now()})

@login_required(login_url='/accounts/login/')
@checkDocuments
@sendToBooking
def opendoor(request,pk):
    renta = get_object_or_404(Booking,status='succeeded', pk=pk,rentor=request.user,paid=True)
    if renta.timeIsUp():
        return redirect('booking:rate',pk=renta.pk)
    device = Devices.objects.filter(flat=renta.flat).first()
    if request.method == 'POST':
        if "open" in request.POST:
            SystemLogs.objects.create(device=device,comment="Нажали кнопку открыть дверь. Статус аренды: {0}".format(renta.timeIsUp()))
            if not renta.timeIsUp():
                print("send signal")
                
                openDoorAPI(device.channel_name,'open',device.secret_key)
            else:
                print("time is up do smth")
            return redirect('booking:opendoor',pk=renta.pk)
    return render(request, 'booking/opendoor.html', {"renta":renta,"device":device})

def trial_booking(request,trial_key):
    renta = get_object_or_404(Booking,trial_key=trial_key)
    if renta.paid is False:
        return redirect("payments:booking",trial_key=trial_key)
    if renta.timeIsUp():
        return redirect('booking:rate',pk=renta.pk)
    device = Devices.objects.filter(flat=renta.flat).first() #get_object_or_404(Devices,flat=renta.flat)
    if request.method == 'POST':
        if "open" in request.POST:
            SystemLogs.objects.create(device=device,comment="Нажали кнопку открыть дверь. Статус аренды: {0}".format(renta.timeIsUp()))
            if not renta.timeIsUp():
                print("send signal")
                openDoorAPI(device.channel_name,'open',device.secret_key)
            else:
                print("time is up do smth")
            return redirect('booking:trial',trial_key=trial_key)
    return render(request, 'booking/opendoor.html', {"renta":renta,"device":device})

def rate(request,pk):
    renta = get_object_or_404(Booking,pk=pk)
    try:
        rentaRaiting = BookingRate.objects.get(booking=renta)
    except:
        rentaRaiting = BookingRate.objects.create(booking=renta,cleanness=8,staff=7)
    if request.method == 'POST':
        form = BookingRateForm(data=request.POST,instance=rentaRaiting)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.rated = True
            rate.save()
            renta.endRenta()
        return redirect('catalog:map')
    form = BookingRateForm(instance=rentaRaiting)
    return render(request, 'booking/rate.html', {"form":form,"booking":renta})

