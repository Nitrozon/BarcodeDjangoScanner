from django.urls import path
from . import views

app_name= "barcode_generator"
urlpatterns = [
    path('generate/<str:code>/', views.generate_barcode, name='generate_barcode'),
    path('generate/', views.generate_code, name='generate_code'),
]