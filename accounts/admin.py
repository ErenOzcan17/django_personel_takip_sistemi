from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, GrupYoneticisi, TakimLideri, MusteriTemsilcisi


class AdminPanel(UserAdmin):
    model = User

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ['USER_TYPE']}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': (
            'first_name', 'last_name', 'email', 'USER_TYPE')}),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'USER_TYPE']


class GrupYoneticisiAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['user__username']
    raw_id_fields = ['user']


class TakimLideriAdmin(admin.ModelAdmin):
    list_display = ['user', 'grup_yoneticisi']
    search_fields = ['user__username', 'grup_yoneticisi__user__username']
    raw_id_fields = ['user', 'grup_yoneticisi']


class MusteriTemsilcisiAdmin(admin.ModelAdmin):
    list_display = ['user', 'takim_lideri']
    search_fields = ['user__username', 'takim_lideri__user__username']
    raw_id_fields = ['user', 'takim_lideri']


admin.site.register(User, AdminPanel)
admin.site.register(GrupYoneticisi, GrupYoneticisiAdmin)
admin.site.register(TakimLideri, TakimLideriAdmin)
admin.site.register(MusteriTemsilcisi, MusteriTemsilcisiAdmin)
