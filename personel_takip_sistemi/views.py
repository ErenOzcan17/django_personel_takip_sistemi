import json
import sqlite3
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from personel_takip_sistemi.decorators import user_is_grup_yoneticisi, user_is_takim_lideri, user_is_musteri_temsilcisi
from personel_takip_sistemi.forms import GorusmeKaydiFormu
from accounts.models import MusteriTemsilcisi, User
from .models import GorusmeKaydi, Primler


@login_required
@user_is_grup_yoneticisi
def grup_yoneticisi_home_view(request):
    return render(request, "app/grup_yoneticisi_home.html")


@login_required
@user_is_takim_lideri
def takim_lideri_home_view(request):
    return render(request, "app/takim_lideri/takim_lideri_home.html")


@login_required
@user_is_takim_lideri
def takim_lideri_itirazlar(request):
    if request.method == 'POST':
        response_data = {}
        try:
            itiraz = Primler.objects.get(id=request.POST.get('id'))
            itiraz.ITIRAZ_DURUM = request.POST.get("itiraz_durum")
            itiraz.ITIRAZ_CEVAP = request.POST.get('itiraz_cevap')
            itiraz.save()
            response_data["error"] = False
            response_data["result"] = "İtiraz başarı ile oluşturuldu"
        except Exception as e:
            response_data["error"] = True
            response_data["result"] = str(e)
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        context = []
        musteri_temsilcileri = MusteriTemsilcisi.objects.filter(TakimLideri_id=request.user.id)
        for musteri_temsilcisi in musteri_temsilcileri:
            musteri_temsilcisi_user = User.objects.get(id=musteri_temsilcisi.user_id)
            itiraz = Primler.objects.filter(MusteriTemsilcisi_id=musteri_temsilcisi.id, ITIRAZ_DURUM='Beklemede')
            context.append({
                'id': itiraz.id,
                'isim': musteri_temsilcisi_user.first_name,
                'soyisim': musteri_temsilcisi_user.last_name,
                'musteri_temsilcisi': musteri_temsilcisi.SICIL_NO,
                'itiraz_aciklama': itiraz.ACIKLAMA,
                'prim_yil': itiraz.PRIM_YIL,
                'prim_ay': itiraz.PRIM_AY,
            })

        return render(request, "app/takim_lideri/itirazlar.html", {"context": context})


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
    if request.method == 'POST':
        response_data = {}
        try:
            prim = Primler.objects.get(id=request.POST.get('id'))
            prim.ITIRAZ_EDILDI = True
            prim.ITIRAZ_DURUM = 'Beklemede'
            prim.ITIRAZ_ACIKLAMA = request.POST.get('itiraz_aciklama')
            prim.save()
            # Todo: Mail gönderme işlemi yapılacak
            response_data["error"] = False
            response_data["result"] = "İtiraz başarı ile oluşturuldu"
        except Exception as e:
            response_data["error"] = True
            response_data["result"] = str(e)
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        musteri_temsilcisi = MusteriTemsilcisi.objects.get(user_id=request.user.id)
        primler = Primler.objects.filter(MusteriTemsilcisi_id=musteri_temsilcisi.id)
        context = []
        for prim in primler:
            context.append({
                'id': prim.id,
                'PRIM_MIKTARI': prim.PRIM_MIKTARI,
                'PRIM_YIL': prim.PRIM_YIL,
                'PRIM_AY': prim.PRIM_AY,
                'ITIRAZ_ACIKLAMA': prim.ITIRAZ_ACIKLAMA,
                'ITIRAZ_DURUM': prim.ITIRAZ_DURUM,
                'ITIRAZ_CEVAP': prim.ITIRAZ_CEVAP,
            })

        return render(request, "app/musteri_temsilcisi/prim_listesi_menusu.html", {"context": context})


@login_required
@user_is_musteri_temsilcisi
def musteri_temsilcisi_primlere_yapilan_itirazlar_menusu(request):
    context = []
    musteri_temsilcisi = MusteriTemsilcisi.objects.get(user_id=request.user.id)
    primler = Primler.objects.filter(MusteriTemsilcisi_id=musteri_temsilcisi.id, ITIRAZ_EDILDI=True)
    for prim in primler:
        context.append({
            'PRIM_MIKTARI': prim.PRIM_MIKTARI,
            'PRIM_YIL': prim.PRIM_YIL,
            'PRIM_AY': prim.PRIM_AY,
            'ITIRAZ_ACIKLAMA': prim.ITIRAZ_ACIKLAMA,
            'ITIRAZ_DURUM': prim.ITIRAZ_DURUM,
            'ITIRAZ_CEVAP': prim.ITIRAZ_CEVAP,
        })
    return render(request, "app/musteri_temsilcisi/primlere_yapilan_itirazlar.html", {"context": context})


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
    return render(request, "app/musteri_temsilcisi/yeni_kayit.html", {"form": form})
