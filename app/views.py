import json
import sqlite3
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from app.decorators import user_is_grup_yoneticisi, user_is_takim_lideri, user_is_musteri_temsilcisi
from app.forms import GorusmeKaydiFormu
from accounts.models import MusteriTemsilcisi, User, TakimLideri
from .models import GorusmeKaydi, Primler


@login_required
@user_is_grup_yoneticisi
def grup_yoneticisi_home_view(request):
    return render(request, "app/grup_yoneticisi_home.html")


@login_required
@user_is_takim_lideri
def takim_lideri_itirazlar(request):
    if request.method == 'POST':
        response_data = {}
        try:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            itiraz = Primler.objects.get(id=body_data['id'])
            itiraz.ITIRAZ_DURUM = body_data['itiraz_durum']
            itiraz.ITIRAZ_CEVAP = body_data['itiraz_cevap']
            itiraz.save()

            # Grup yöneticisine e-posta gönderme
            # grup_yoneticisi_email = 'group_manager@example.com'  # Grup yöneticisinin e-posta adresi
            # send_mail(
            #     'İtiraz Durumu Güncellendi',
            #     f'İtiraz ID: {itiraz.id}\nDurum: {itiraz.ITIRAZ_DURUM}\nCevap: {itiraz.ITIRAZ_CEVAP}',
            #     'from@example.com',
            #     [grup_yoneticisi_email],
            #     fail_silently=False,
            # )

            response_data["error"] = False
            response_data["result"] = "İtiraz başarı ile güncellendi"
        except Exception as e:
            response_data["error"] = True
            response_data["result"] = str(e)
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        context = []
        musteri_temsilcileri = MusteriTemsilcisi.objects.filter(takim_lideri_id=request.user.id)
        for musteri_temsilcisi in musteri_temsilcileri:
            user = User.objects.get(id=musteri_temsilcisi.user_id)
            itirazlar = Primler.objects.filter(MusteriTemsilcisi_id=user.id, ITIRAZ_EDILDI=True)
            for itiraz in itirazlar:
                context.append({
                    'id': itiraz.id,
                    'sicil_no': musteri_temsilcisi.SICIL_NO,
                    'isim': user.first_name,
                    'soyisim': user.last_name,
                    'itiraz_aciklama': itiraz.ITIRAZ_ACIKLAMA,
                    'prim_yil': itiraz.PRIM_YIL,
                    'prim_ay': itiraz.PRIM_AY,
                    'itiraz_durum': itiraz.ITIRAZ_DURUM,
                    'itiraz_cevaplandı': itiraz.ITIRAZ_CEVAPLANDI,
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
            json_data = json.loads(request.body)
            prim = Primler.objects.get(id=json_data['id'])
            prim.ITIRAZ_EDILDI = True
            prim.ITIRAZ_DURUM = 'Beklemede'
            prim.ITIRAZ_ACIKLAMA = json_data['itiraz_aciklama']
            prim.save()
            # Todo: Mail gönderme işlemi yapılacak
            response_data["error"] = False
            response_data["result"] = "İtiraz başarı ile oluşturuldu"
        except Exception as e:
            response_data["error"] = True
            response_data["result"] = str(e)
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        primler = Primler.objects.filter(MusteriTemsilcisi_id=request.user.id)
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
                'ITIRAZ_EDILDI': prim.ITIRAZ_EDILDI,
                'ITIRAZ_CEVAPLANDI': prim.ITIRAZ_CEVAPLANDI,
            })

        return render(request, "app/musteri_temsilcisi/prim_listesi_menusu.html", {"context": context})


@login_required
@user_is_musteri_temsilcisi
def musteri_temsilcisi_primlere_yapilan_itirazlar_menusu(request):
    context = []
    primler = Primler.objects.filter(MusteriTemsilcisi_id=request.user.id, ITIRAZ_EDILDI=True)
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
                GorusmeKaydi.objects.create(
                    Musteri_ad=form.cleaned_data['Musteri_ad'],
                    Musteri_soyad=form.cleaned_data['Musteri_soyad'],
                    GORUSME_KONU=form.cleaned_data['GORUSME_KONU'],
                    GORUSME_DURUMU=form.cleaned_data['GORUSME_DURUMU'],
                    GORUSME_BASLANGIC_TARIHI=form.cleaned_data['GORUSME_BASLANGIC_TARIHI'],
                    GORUSME_BITIS_TARIHI=form.cleaned_data['GORUSME_BITIS_TARIHI'],
                    MusteriTemsilcisi_id=request.user.id
                )
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



