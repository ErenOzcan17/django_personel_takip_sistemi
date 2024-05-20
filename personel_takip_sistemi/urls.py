from . import views
from django.urls import path

urlpatterns = [
    path('musteri/', views.musteri_home_view, name='musteri_home'),
]