from django.shortcuts import render


def service_details(request):
    return render(request, "service-details.html")