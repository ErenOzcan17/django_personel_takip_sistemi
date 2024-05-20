import json
import sqlite3
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from personel_takip_sistemi.decorators import user_is_grup_yoneticisi, user_is_takim_lideri, user_is_musteri_temsilcisi
from personel_takip_sistemi.forms import GorusmeKaydiFormu
from .models import GorusmeKaydi


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
    return render(request, "app/musteri_temsilcisi/home.html")


@login_required
@user_is_musteri_temsilcisi
def musteri_temsilcisi_cagri_listesi_menusu(request):
    context = []
    kayitlar = GorusmeKaydi.objects.all()
    for kayit in kayitlar:
        context.append({
            'Musteri_ad': kayit.Musteri_ad,
            'Musteri_soyad': kayit.Musteri_soyad,
            'GORUSME_KONU': kayit.GORUSME_KONU,
            'GORUSME_DURUMU': kayit.GORUSME_DURUMU,
            'GORUSME_BASLANGIC_TARIHI': kayit.GORUSME_BASLANGIC_TARIHI,
            'GORUSME_BITIS_TARIHI': kayit.GORUSME_BITIS_TARIHI,
        })
    return render(request, 'app/musteri_temsilcisi/gorusme_kaydı.html', {'context': kayitlar})


@login_required
@user_is_musteri_temsilcisi
def musteri_temsilcisi_aylik_prim_listesi_menusu(request):
    return render(request, "app/musteri_temsilcisi/home.html")


@login_required
@user_is_musteri_temsilcisi
def musteri_temsilcisi_primlere_yapilan_itirazlar_menusu(request):
    return render(request, "app/musteri_temsilcisi/home.html")


@login_required
@user_is_musteri_temsilcisi
def musteri_temsilcisi_yeni_kayit(request):
    if request.method == 'POST':
        response_data = {}
        form = GorusmeKaydiFormu(request.POST)
        try:
            if form.is_valid():
                form.save()
                response_data["error"] = False
                response_data["result"] = "Kayıt başarı ile oluşturuldu"
            else:
                response_data["error"] = True
                response_data["result"] = "Form is not valid"
        except Exception as e:
            response_data["error"] = True
            response_data["result"] = str(e)
    else:
        form = GorusmeKaydiFormu()
    return render(request, "app/musteri_temsilcisi/yeni_kayit.html", {'form': form})
