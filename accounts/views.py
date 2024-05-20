import json
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import LoginForm


def index(request):
    return render(request, "accounts/index.html")


def login_view(request):
    if request.method == "POST":
        response_data = {}
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                if user.USER_TYPE == "Musteri":
                    response_data["redirect_url"] = reverse("musteri_home")
                if user.USER_TYPE == "GrupYoneticisi":
                    response_data["redirect_url"] = reverse("grup_yoneticisi_home")
                if user.USER_TYPE == "TakimLideri":
                    response_data["redirect_url"] = reverse("takim_lideri_home")
                if user.USER_TYPE == "MusteriTemsilcisi":
                    response_data["redirect_url"] = reverse("musteri_temsilcisi_home")
                response_data["error"] = False
                response_data["result"] = "User is authenticated"
            else:
                response_data["error"] = True
                response_data["result"] = "Email or password is wrong"
        else:
            response_data["error"] = True
            response_data["result"] = "Form is not valid"
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("index")
