from django import forms
from .models import GorusmeKaydi, Primler


class GorusmeKaydiFormu(forms.ModelForm):
    class Meta:
        model = GorusmeKaydi
        fields = [
            'Musteri_ad',
            'Musteri_soyad',
            'GORUSME_KONU',
            'GORUSME_DURUMU',
            'GORUSME_BASLANGIC_TARIHI',
            'GORUSME_BITIS_TARIHI'
        ]
        widgets = {
            'GORUSME_BASLANGIC_TARIHI': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'GORUSME_BITIS_TARIHI': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }
