from django.test import TestCase
from django.contrib.auth.models import User
from payments.models import Transactions


#auto payment
t =  Transactions.yandex.createPayment(
    User.objects.get(pk=1),
    100,
    payment_type=True
)
transaction = Transactions.objects.get(payment_id=t.id)
transaction.capture()
transaction.setInfo(transaction.getInfo())
transaction.checkout()
print(transaction.status)