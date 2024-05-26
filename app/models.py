from django.db import models
from accounts.models import MusteriTemsilcisi, TakimLideri, GrupYoneticisi


class GorusmeKaydi(models.Model):
    id = models.AutoField(primary_key=True)
    Musteri_ad = models.CharField(max_length=100)
    Musteri_soyad = models.CharField(max_length=100)
    MusteriTemsilcisi = models.ForeignKey(MusteriTemsilcisi, on_delete=models.CASCADE)
    GORUSME_KONU_CHOICES = [
        ('Arıza', 'Arıza'),
        ('Talep', 'Talep'),
        ('Bilgi', 'Bilgi')
    ]
    GORUSME_KONU = models.CharField(max_length=10, choices=GORUSME_KONU_CHOICES)
    GORUSME_DURUMU_CHOICES = [
        ('Tamamlandı', 'Tamamlandı'),
        ('Takip ediliyor', 'Takip ediliyor'),
        ('Sorun çözülemedi', 'Sorun çözülemedi')
    ]
    GORUSME_DURUMU = models.CharField(max_length=20, choices=GORUSME_DURUMU_CHOICES)
    GORUSME_BASLANGIC_TARIHI = models.DateTimeField()
    GORUSME_BITIS_TARIHI = models.DateTimeField()


class Primler(models.Model):
    MusteriTemsilcisi = models.ForeignKey(MusteriTemsilcisi, on_delete=models.CASCADE)
    ITIRAZ_EDILDI = models.BooleanField()
    ITIRAZ_CEVAPLANDI = models.BooleanField()
    ITIRAZ_DURUM_CHOISES = [
        ('Beklemede', 'Beklemede'),
        ('Onaylandı', 'Onaylandı'),
        ('Reddedildi', 'Reddedildi')
    ]
    ITIRAZ_DURUM = models.CharField(max_length=20, choices=ITIRAZ_DURUM_CHOISES, blank=True, null=True)
    PRIM_YIL = models.IntegerField()
    PRIM_AY_CHOISES = [
        ('Ocak', 'Ocak'),
        ('Şubat', 'Şubat'),
        ('Mart', 'Mart'),
        ('Nisan', 'Nisan'),
        ('Mayıs', 'Mayıs'),
        ('Haziran', 'Haziran'),
        ('Temmuz', 'Temmuz'),
        ('Ağustos', 'Ağustos'),
        ('Eylül', 'Eylül'),
        ('Ekim', 'Ekim'),
        ('Kasım', 'Kasım'),
        ('Aralık', 'Aralık'),
    ]
    PRIM_AY = models.CharField(max_length=20, choices=PRIM_AY_CHOISES)
    PRIM_MIKTARI = models.FloatField()
    ITIRAZ_ACIKLAMA = models.TextField(blank=True, null=True)
    ITIRAZ_CEVAP = models.TextField(blank=True, null=True)
