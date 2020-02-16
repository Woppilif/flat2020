from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('settings/', views.settings, name='settings'),
    path('settings/card/delete', views.settings_delcard, name='settings_delcard'),
    path('registration/', views.registration, name='registration'),
    path('documents/', views.documents, name='documents'),
    
    #path('payment/<str:id>', views.capture, name='capture'),
] 