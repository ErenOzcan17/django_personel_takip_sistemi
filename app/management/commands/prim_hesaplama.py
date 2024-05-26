from datetime import datetime
from django.core.management.base import BaseCommand
from app.models import GorusmeKaydi


class Command(BaseCommand):
    help = 'mevcut ayın primlerini hesaplar'

    def handle(self, *args, **kwargs):
        year = datetime.now().year
        month = datetime.now().month
        month_start = datetime(year, month, 1)
        month_end = datetime(year, month, 31, 23, 59, 59)

        gorusme_kayitlari = GorusmeKaydi.objects.filter(GORUSME_BASLANGIC_TARIHI__gte=month_start,
                                                        GORUSME_BITIS_TARIHI__lte=month_end)

        musteri_temsilcisileri = GorusmeKaydi.objects.values('MusteriTemsilcisi').distinct()


        for musteri_temsilcisi in musteri_temsilcisileri:
            musteri_temsilcisi_id = musteri_temsilcisi['MusteriTemsilcisi']
            musteri_temsilcisi_gorusmeleri = gorusme_kayitlari.filter(MusteriTemsilcisi=musteri_temsilcisi_id)
            toplam_gorusme_sayisi = musteri_temsilcisi_gorusmeleri.count()
            print(f'{musteri_temsilcisi_id} sicil numaralı müşteri temsilcisi {toplam_gorusme_sayisi} adet görüşme yapmıştır.')
