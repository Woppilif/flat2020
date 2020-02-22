from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from payments.models import Transactions
from booking.models import Booking
# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
    t =  Transactions.yandex.createPayment(
        request.user,
        1,
        payment_type="account"
    )
    #print(t.status)
    #print(t.payment_type)
    return render(request, 'payment.html', {'transaction':t})

#@login_required(login_url='/accounts/login/')
def capture(request,id):
    print(id)
    transaction = get_object_or_404(Transactions,checkouted = False, payment_id = id)
    transaction.setInfo(transaction.getInfo())
    print(transaction.status)
    print(transaction.payment_type)
    if transaction.status == "waiting_for_capture":
        print("here wfc")
        if transaction.payment_type == "account":
            print("here acc")
            transaction.checkout()
            return redirect('catalog:map')
        elif transaction.payment_type == "trial":
            transaction.capture()
            transaction.setInfo(transaction.getInfo())
            transaction.checkout()
            return redirect('booking:trial',trial_key=transaction.booking.trial_key)
        else:
            transaction.capture()
            transaction.setInfo(transaction.getInfo())
            return redirect('catalog:map')
    if transaction.status == "pending":
        return redirect('payments:index')
    if transaction.status == "succeeded":
        transaction.checkout()
    if transaction.status == "canceled":
        return render(request, 'error.html', {})
    return redirect('catalog:map')

def booking_pay(request,trial_key):
    booking = get_object_or_404(Booking,trial_key=trial_key)
    t =  Transactions.yandex.createPayment(
        user=booking.rentor,
        amount=booking.getPrice(),
        booking=booking,
        payment_type='trial'
    )
    return render(request, 'booking.html', {'transaction':t,"booking":booking})