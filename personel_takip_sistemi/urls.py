from . import views
from django.urls import path, include

urlpatterns = [
    path(
        "grup_yoneticisi/",
        include(
            [
                path("", views.grup_yoneticisi_home_view, name='grup_yoneticisi_home'),
            ]
        )
    ),

    path(
        "takim_lideri_home/",
        include(
            [
                path("", views.takim_lideri_home_view, name='takim_lideri_home'),
            ]
        )
    ),

    path(
        "musteri_temsilcisi/",
        include(
            [
                path("", views.musteri_temsilcisi_home_view, name='musteri_temsilcisi_home'),
                path("cagri_listesi_menu/", views.musteri_temsilcisi_cagri_listesi_menusu, name="cagri_listesi_menu"),
                path("aylik_prim_listesi_menu/", views.musteri_temsilcisi_aylik_prim_listesi_menusu,
                     name="aylik_prim_listesi_menu"),
                path("yapilan_itirazlar/", views.musteri_temsilcisi_primlere_yapilan_itirazlar_menusu,
                     name="yapilan_itirazlar_menu"),
                path("yeni_kayit/", views.musteri_temsilcisi_yeni_kayit, name="yeni_kayit"),
            ]
        )
    ),
]
