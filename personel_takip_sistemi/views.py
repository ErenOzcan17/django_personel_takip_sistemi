from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from personel_takip_sistemi.decorators import (user_is_musteri, user_is_grup_yoneticisi,
                                               user_is_takim_lideri, user_is_musteri_temsilcisi)


@login_required
@user_is_grup_yoneticisi
def grup_yoneticisi_home_view(request):
    return render(request, "app/grup_yoneticisi_home.html")


@login_required
@user_is_takim_lideri
def takim_lideri_home_view(request):
    return render(request, "app/takim_lideri_home.html")


@login_required
@user_is_musteri_temsilcisi
def musteri_temsilcisi_home_view(request):
    return render(request, "app/musteri_temsilcisi_home.html")


@login_required
@user_is_musteri
def musteri_home_view(request):
    return render(request, "app/musteri_home.html")
