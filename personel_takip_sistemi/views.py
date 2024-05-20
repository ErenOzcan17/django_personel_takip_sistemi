from django.shortcuts import render


def musteri_home_view(request):
    return render(request, "musteri_home.html")