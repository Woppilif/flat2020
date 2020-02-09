from django.test import TestCase
from django.contrib.auth.models import User
from payments.models import Transactions
'''
t =  Transactions.yandex.createPayment(
    User.objects.get(pk=1),
    100,
    payment_type=False
)

print(t)
'''
i = Transactions.yandex.getInfo('25d25ec4-000f-5000-a000-1db4f928568c')
print(i.status)