from django.urls import path
from booking import views

app_name = 'booking'

urlpatterns = [
    path('<int:pk>/', views.index, name='act'),
]