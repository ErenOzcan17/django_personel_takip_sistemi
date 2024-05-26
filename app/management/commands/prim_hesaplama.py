from datetime import datetime
import calendar
from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import MusteriTemsilcisi
from app.models import GorusmeKaydi, Primler


class Command(BaseCommand):
    help = 'mevcut ayın primlerini hesaplar'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        year = now.year
        month = now.month
        _, last_day = calendar.monthrange(year, month)
        month_start = timezone.make_aware(datetime(year, month, 1))
        month_end = timezone.make_aware(datetime(year, month, last_day, 23, 59, 59))

        tum_gorusme_kayitlari = GorusmeKaydi.objects.filter(GORUSME_BASLANGIC_TARIHI__gte=month_start,
                                                             GORUSME_BITIS_TARIHI__lte=month_end)

        musteri_temsilcisileri = MusteriTemsilcisi.objects.all()
        musteri_temsilcisi_primleri = []

        for musteri_temsilcisi in musteri_temsilcisileri:
            musteri_temsilcisi_prim = 5000
            gorusme_gunleri = [0] * 31  # 31 günlük bir liste oluşturuyoruz
            gorusme_kayitlari = tum_gorusme_kayitlari.filter(MusteriTemsilcisi_id=musteri_temsilcisi.user_id)
            for gorusme_kaydi in gorusme_kayitlari:
                gorusme_gunu = gorusme_kaydi.GORUSME_BASLANGIC_TARIHI.day
                gorusme_gunleri[gorusme_gunu - 1] += 1  # İndeks 0'dan başladığı için gün sayısını 1 azaltıyoruz
            for i in range(0, 31):  # İndekslerin doğru olması için 0'dan başlıyoruz
                if gorusme_gunleri[i] > 0:
                    if gorusme_gunleri[i] < 100:
                        musteri_temsilcisi_prim += 0
                    elif 100 <= gorusme_gunleri[i] < 200:
                        musteri_temsilcisi_prim += gorusme_gunleri[i] * 1.25
                    else:
                        musteri_temsilcisi_prim += gorusme_gunleri[i] * 2
            musteri_temsilcisi_primleri.append({
                'musteri_temsilcisi': musteri_temsilcisi,
                'prim': musteri_temsilcisi_prim
            })
        for musteri_temsilcisi_prim in musteri_temsilcisi_primleri:
            prim = Primler.objects.create(
                MusteriTemsilcisi=musteri_temsilcisi_prim['musteri_temsilcisi'],
                PRIM_YIL=year,
                PRIM_AY=month,
                PRIM_MIKTARI=musteri_temsilcisi_prim['prim'],
                ITIRAZ_EDILDI=False,
                ITIRAZ_CEVAPLANDI=False,
            )
            prim.save()
