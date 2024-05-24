from django import forms
from django.contrib.auth.admin import UserAdmin
from .models import User, GrupYoneticisi, TakimLideri, MusteriTemsilcisi
from django.contrib import admin


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserAdminForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['sorumlu_takim_lideri'].queryset = User.objects.filter(USER_TYPE='TakimLideri')
            self.fields['sorumlu_grup_yoneticisi'].queryset = User.objects.filter(USER_TYPE='GrupYoneticisi')


class AdminPanel(UserAdmin):
    form = UserAdminForm
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ['USER_TYPE']}),
        ('Others', {'fields': ('sorumlu_takim_lideri', 'sorumlu_grup_yoneticisi')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('first_name', 'last_name', 'email', 'USER_TYPE', 'sorumlu_takim_lideri', 'sorumlu_grup_yoneticisi')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'sorumlu_takim_lideri', 'sorumlu_grup_yoneticisi')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.USER_TYPE == 'GrupYoneticisi':
            GrupYoneticisi.objects.get_or_create(user=obj)
        # elif obj.USER_TYPE == 'TakimLideri':
        #     obj.save()
        #     TakimLideri.objects.get_or_create(user=obj, grup_yoneticisi_id=obj.sorumlu_grup_yoneticisi_id)
        # elif obj.USER_TYPE == 'MusteriTemsilcisi':
        #     obj.save()
        #     MusteriTemsilcisi.objects.get_or_create(user=obj, takim_lideri_id=obj.sorumlu_takim_lideri_id)


admin.site.register(User, AdminPanel)
