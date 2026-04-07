"""
URL configuration for mini_jira project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# Cette fonction va attraper les gens qui arrivent sur la page d'accueil vide
def redirect_to_login(request):
    return redirect('login')

urlpatterns = [
    # 1. LA RACINE : Si l'URL est vide, on redirige vers le login
    path('', redirect_to_login, name='root_redirect'),

    # 2. TES APPLICATIONS
    path('admin/', admin.site.urls),
    path('projects/', include('projects.urls')),
    path('accounts/', include('accounts.urls')),
    path("tickets/", include("tickets.urls")),
    path('sprints/', include('sprints.urls')),
]