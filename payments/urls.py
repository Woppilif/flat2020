from django.urls import path
from payments import views

app_name = 'payments'

urlpatterns = [
    path('payment/', views.index, name='index'),
    path('payment/<str:id>', views.capture, name='capture'),
    path('booking/<uuid:trial_key>', views.booking_pay, name='booking'),
    #path('error/', views.error, name='error'),
]