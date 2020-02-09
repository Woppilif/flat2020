from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from payments.models import Transactions
# Create your views here.
def index(request):
    t =  Transactions.yandex.createPayment(
        request.user,
        100
    )
    return render(request, 'payment.html', {'transaction':t})

def capture(request,id):
    transaction = get_object_or_404(Transactions, payment_id = id)
    transaction.setInfo(Transactions.yandex.getInfo(id))
    return HttpResponse(transaction.status)

#TO/DO
#create userdocuments
#save payment meth
#test autopayment
#unlink card
#exclude transaction flood