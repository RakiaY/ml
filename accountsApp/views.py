from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import admin_only


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            # Redirection selon le groupe de l'utilisateur
            if user.groups.filter(name='Admin').exists():
                return redirect("dashboard")  # Admin → Dashboard
            elif user.groups.filter(name='Client').exists():
                return redirect("women_preference")  # Client → Modèle ML
            else:
                return redirect("login")  # Pas de groupe → Retour login
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "dashboard/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@admin_only
def dashboard(request):
    return render(request, "dashboard/index.html")
