from django.urls import path
from . import views

app_name = 'Registration'
urlpatterns = [
    path('scan/', views.scan_barcode, name='scan_barcode'),
    path('img/', views.image_upload, name='image_upload'),
]