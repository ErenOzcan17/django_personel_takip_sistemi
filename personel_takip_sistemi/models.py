from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPE_CHOISES = [
        ('GrupYoneticisi', 'GrupYoneticisi'),
        ('TakimLideri', 'TakimLideri'),
        ('MusteriTemsilcisi', 'MusteriTemsilcisi'),
    ]
    USER_TYPE = models.CharField(max_length=30, choices=USER_TYPE_CHOISES)

    def __str__(self):
        return self.username


class GrupYoneticisi(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class TakimLideri(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    GrupYoneticisi = models.ForeignKey(GrupYoneticisi, on_delete=models.CASCADE)


class MusteriTemsilcisi(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    TakimLideri = models.ForeignKey(TakimLideri, on_delete=models.CASCADE)
    SICIL_NO = models.CharField(max_length=11, unique=True)


class GorusmeKaydi(models.Model):
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
    ITIRAZ_DURUM_CHOISES = [
        ('Beklemede', 'Beklemede'),
        ('Onaylandı', 'Onaylandı'),
        ('Reddedildi', 'Reddedildi')
    ]
    ITIRAZ_DURUM = models.CharField(max_length=20, choices=ITIRAZ_DURUM_CHOISES)
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
    ITIRAZ_ACIKLAMA = models.TextField()
    ITIRAZ_CEVAP = models.TextField()
