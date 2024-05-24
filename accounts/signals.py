from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, GrupYoneticisi, TakimLideri, MusteriTemsilcisi


@receiver(post_save, sender=User)
def create_grup_yoneticisi(sender, instance, created, **kwargs):
    if created and instance.USER_TYPE == 'GrupYoneticisi':
        grup_yoneticisi = GrupYoneticisi.objects.create(user_grup=instance)
        grup_yoneticisi.save()
    elif created and instance.USER_TYPE == 'TakimLideri':
        takim_lideri = TakimLideri.objects.create(user_takim=instance,
                                                  grup_yoneticisi=instance.sorumlu_grup_yoneticisi)
        takim_lideri.save()
    elif created and instance.USER_TYPE == 'MusteriTemsilcisi':
        musteri_temsilcisi = MusteriTemsilcisi.objects.create(user_musteri=instance,
                                                              takim_lideri=instance.sorumlu_takim_lideri)
        musteri_temsilcisi.save()
