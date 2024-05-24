from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('GrupYoneticisi', 'GrupYoneticisi'),
        ('TakimLideri', 'TakimLideri'),
        ('MusteriTemsilcisi', 'MusteriTemsilcisi'),
    ]
    USER_TYPE = models.CharField(max_length=30, choices=USER_TYPE_CHOICES)
    sorumlu_takim_lideri = models.OneToOneField('self', on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='takim_lideri_user', limit_choices_to={'USER_TYPE': 'TakimLideri'})
    sorumlu_grup_yoneticisi = models.OneToOneField('self', on_delete=models.SET_NULL, null=True, blank=True,
                                           related_name='grup_yoneticisi_user', limit_choices_to={'USER_TYPE': 'GrupYoneticisi'})

    def __str__(self):
        return self.username


class GrupYoneticisi(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class TakimLideri(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    grup_yoneticisi = models.ForeignKey(GrupYoneticisi, on_delete=models.CASCADE)


class MusteriTemsilcisi(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    takim_lideri = models.ForeignKey(TakimLideri, on_delete=models.CASCADE)
    SICIL_NO = models.CharField(max_length=11, unique=True)
