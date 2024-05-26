from django.core.exceptions import PermissionDenied


def user_is_grup_yoneticisi(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.USER_TYPE == "GrupYoneticisi" or user.is_superuser == True:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def user_is_takim_lideri(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.USER_TYPE == "TakimLideri" or user.is_superuser == True:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def user_is_musteri_temsilcisi(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.USER_TYPE == "MusteriTemsilcisi" or user.is_superuser == True:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap
