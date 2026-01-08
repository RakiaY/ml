"""
Décorateurs pour gérer le contrôle d'accès basé sur les groupes
"""

from functools import wraps
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages


def admin_only(view_func):
    """
    Décorateur pour restreindre l'accès aux administrateurs uniquement.
    Les utilisateurs non-admin sont déconnectés et redirigés.
    """
    @wraps(view_func)
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):
        # Vérifier si l'utilisateur est dans le groupe Admin
        if request.user.groups.filter(name='Admin').exists():
            return view_func(request, *args, **kwargs)
        else:
            # Déconnecter l'utilisateur
            from django.contrib.auth import logout
            logout(request)
            messages.error(request, "Accès refusé. Vous avez été déconnecté.")
            return redirect('login')
    
    return wrapper


def client_or_admin(view_func):
    """
    Décorateur pour permettre l'accès aux clients et aux admins.
    """
    @wraps(view_func)
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):
        # Vérifier si l'utilisateur est dans le groupe Admin ou Client
        if request.user.groups.filter(name__in=['Admin', 'Client']).exists():
            return view_func(request, *args, **kwargs)
        else:
            # Déconnecter l'utilisateur
            from django.contrib.auth import logout
            logout(request)
            messages.error(request, "Accès refusé. Vous avez été déconnecté.")
            return redirect('login')
    
    return wrapper
