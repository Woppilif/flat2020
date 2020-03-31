from django.urls import path
from managing import views

app_name = 'managing'

urlpatterns = [
    path('flats/', views.flats, name='flats'),
    path('flat/<int:pk>', views.flat, name='flat'),
    path('', views.index, name='index'),
    path('create/', views.trial_create, name='trial_create'),
    path('trials/', views.trials, name='trials'),
    path('users/', views.users, name='users'),
    path('user/<int:pk>', views.user_page, name='user'),
    path('reviews/', views.reviews, name='reviews'),
    path('requests/', views.requests, name='requests'),
    path('devices/', views.devices, name='devices'),
    path('booking/<int:pk>', views.rentaInfo, name='booking'),
    path('telegram/<uuid:token>', views.telegram, name='telegram'),
    
]