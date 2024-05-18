from . import views
from django.urls import path

urlpatterns = [
    path('', views.service_details, name='index'),
]