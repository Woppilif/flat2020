from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models import Q
from django.utils.timezone import now
from yandex_checkout import Payment,Configuration 
from django.conf import settings
# Create your models here.
Configuration.account_id = settings.YA_ACCOUNT_ID
Configuration.secret_key = settings.YA_SECRET_KEY

class YandexPayments(models.Manager):

    def getCurrentTransaction(self,user,amount,booking=None,payment_type="account"):
        return self.filter(Q(status="pending") | Q(status="waiting_for_capture"),user=user,checkouted=False,price=amount,booking=booking,payment_type = payment_type).last()

    def createPayment(self,user,amount,booking=None,payment_type="account"):
        '''
            Create yandex kassa payment object. payment_type = True - autopayment otherwise is add card
        '''
        if self.getCurrentTransaction(user,amount,booking,payment_type) is not None:
            print("Yes getCurrentTransaction")
            return self.getCurrentTransaction(user,amount,booking,payment_type).getInfo()
        payment_info = {
            "amount": {
                "value": amount,
                "currency": "RUB"
            },
            "description": "Привязка карты"
        }
        payment_info.update(self.createReceipt(user,amount))
        if payment_type == "full":
            payment_info.update(self.createAutoPayment(user))
        else: #payment_type == "account": # False
            payment_info.update(self.createConfirmation())
        payment_object = Payment.create(payment_info)
        self.create(
            user = user,
            booking = booking,
            price = amount,
            date = now(),
            status = payment_object.status,
            payment_type = payment_type,
            payment_id = payment_object.id,
            created_at = payment_object.created_at,
            expires_at = payment_object.expires_at,
            checkouted = False
        )
        return payment_object

    def createAutoPayment(self,user):
        return {
            "payment_method_id": user.documents.yakey
        }

    def createConfirmation(self):
        return {
            "confirmation": {
                "type": "embedded"
            },
            "capture": False,
            "save_payment_method": True,
        }

    def createReceipt(self,user,amount):
        return {
            "receipt": {
            "customer": {
                "full_name": "{0} {1}".format(user.first_name,user.last_name),
                "email": user.email,
            },
            "items": [
                    {
                        "description": "Оплата аренды",
                        "quantity": "1.00",
                        "amount": {
                            "value": amount,
                            "currency": "RUB"
                        },
                        "vat_code": "0",
                        "payment_mode": "full_payment",
                        "payment_subject": "service"
                    }
                ]
            }
        }


class Transactions(models.Model):
    P_TYPES = (
        ('account', 'Привязка карты'),
        ('deposit', 'Депозит'),
        ('full', 'Полная стоимость'),
        ('usercard', 'Оплата картой клиента'),
        ('trial', 'Оплата аренды без регистрации')
    )
    PAID_TYPES = (
        ('pending', 'Создан'), # Статус сразу после создания аренды
        ('waiting_for_capture', 'Ожидает подтверждения от пользователя'), #Был начат осмотр кв
        ('succeeded', 'Успешно оплачен'), # Успешно оплачена
        ('canceled', 'Отменен') # отказ клиентом от аренды
    )
    user = models.ForeignKey(User, models.DO_NOTHING,blank=True, null=True)
    booking = models.ForeignKey('booking.Booking', on_delete=models.CASCADE,blank=True, null=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    date = models.DateTimeField(null=True,blank=True)
    status = models.CharField(max_length=40,null=True,default='pending',choices=PAID_TYPES)
    payment_type = models.CharField(max_length=40,blank=True, null=True,choices=P_TYPES,default='account')
    payment_id = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(null=True,blank=True)
    expires_at = models.DateTimeField(null=True,blank=True)
    captured_at = models.DateTimeField(null=True,blank=True)
    checkouted = models.BooleanField(null=False,default=False,blank=False)

    yandex = YandexPayments()
    objects = models.Manager()

    class Meta:
        verbose_name = 'Транзакции'
        verbose_name_plural = 'Транзакции'

    def __str__(self):
        return "{0}. Дата и время создания: {1}".format(self.price,self.date)

    def setInfo(self,paymentObject):
        self.payment_id = paymentObject.id
        self.status = paymentObject.status
        self.created_at = paymentObject.created_at
        self.expires_at = paymentObject.expires_at
        self.save()
        return self

    def capture(self):
        return Payment.capture(
            self.payment_id,
            {
                "amount": {
                    "value": self.price,
                    "currency": "RUB"
                }
            },
            str(uuid.uuid4()) #idempotence key
        )

    def getInfo(self):
        return Payment.find_one(self.payment_id)

    def cancel(self):
        Payment.cancel(self.payment_id,str(uuid.uuid4()))

    def checkout(self):
        if self.checkouted == True:
            return False
        if self.payment_type == "account":
            self.cancel()
            self.setInfo(self.getInfo())
            self.user.documents.addCard(self.getInfo())
            self.checkouted = True
            self.save()
            return True
        else:
            self.booking.activate()
            self.checkouted = True
            self.save()
            return True
        return False
        



    