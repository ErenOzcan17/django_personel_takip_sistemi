from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('GrupYoneticisi', 'GrupYoneticisi'),
        ('TakimLideri', 'TakimLideri'),
        ('MusteriTemsilcisi', 'MusteriTemsilcisi'),
    ]
    USER_TYPE = models.CharField(max_length=30, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return self.username


class GrupYoneticisi(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


class TakimLideri(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    grup_yoneticisi = models.ForeignKey(GrupYoneticisi, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class MusteriTemsilcisi(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    takim_lideri = models.ForeignKey(TakimLideri, on_delete=models.CASCADE)
    SICIL_NO = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return self.user.username
