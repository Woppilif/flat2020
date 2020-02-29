from django.urls import path
from catalog import views
from managing.views import device
app_name = 'catalog'

urlpatterns = [
    path('map/', views.map, name='map'),
    path('list/', views.clist, name='list'),
    path('list/<int:offset>', views.clist, name='list'),
    path('apartment/<int:pk>', views.apartment, name='apartment'),
    path('device/<uuid:dkey>', device, name='device'),
    path('', views.index, name='index'),
    path('rules/', views.user_agreement, name='user_agreement'),
    path('agreement/', views.agreement, name='agreement'),
]