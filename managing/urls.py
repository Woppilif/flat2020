from django.urls import path
from managing import views

app_name = 'managing'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.trial_create, name='trial_create'),
]