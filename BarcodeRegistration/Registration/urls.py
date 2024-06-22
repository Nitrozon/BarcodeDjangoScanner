from django.urls import path
from . import views

app_name = 'Registration'
urlpatterns = [
    path('scan/', views.scan_barcode, name='scan_barcode'),
]