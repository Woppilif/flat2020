from django.urls import path
from managing import views

app_name = 'managing'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.trial_create, name='trial_create'),
    path('trials/', views.trials, name='trials'),
    path('users/', views.users, name='users'),
    path('requests/', views.requests, name='requests'),
    path('devices/', views.devices, name='devices'),
    path('booking/<int:pk>', views.rentaInfo, name='booking'),
    
]