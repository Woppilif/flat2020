from django.urls import path
from booking import views

app_name = 'booking'

urlpatterns = [
    path('<int:pk>/', views.opendoor, name='opendoor'),
    path('act/<int:pk>', views.index, name='act'),
    path('trial/<uuid:trial_key>', views.trial_booking, name='trial'),
    path('rate/<int:pk>', views.rate, name='rate'),
    
]