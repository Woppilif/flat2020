from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from payments.models import Transactions
# Create your views here.
def index(request):
    t =  Transactions.yandex.createPayment(
        request.user,
        100
    )
    print(t.id)
    return render(request, 'payment.html', {'transaction':t})

def capture(request,id):
    transaction = get_object_or_404(Transactions,checkouted = False, payment_id = id)
    transaction.setInfo(transaction.getInfo())
    if transaction.status == "waiting_for_capture":
        if transaction.payment_type == "account":
            transaction.checkout()
        else:
            transaction.capture()
            transaction.setInfo(transaction.getInfo())
    if transaction.status == "pending":
        return redirect('payments:index')
    if transaction.status == "succeeded":
        transaction.checkout()
    return HttpResponse(transaction.status)

#TO/DO
#create userdocuments +
#save payment meth +
#test autopayment +
#unlink card +/-
#exclude transaction flood +
#booking checkout +


#TO/DO
