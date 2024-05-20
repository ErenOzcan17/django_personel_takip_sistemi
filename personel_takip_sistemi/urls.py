from . import views
from django.urls import path

urlpatterns = [
    path('musteri/', views.musteri_home_view, name='musteri_home'),
    path('grup_yoneticisi/', views.grup_yoneticisi_home_view, name='grup_yoneticisi_home'),
    path('takim_lideri_home/', views.takim_lideri_home_view, name='takim_lideri_home'),
    path('musteri_temsilcisi/', views.musteri_temsilcisi_home_view, name='musteri_temsilcisi_home'),
]