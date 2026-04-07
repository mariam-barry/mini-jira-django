from django.urls import path
from django.contrib.auth import views as auth_views # Outils Django
from . import views

urlpatterns = [
    # CONNEXION : On utilise l'outil de Django 
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    
    # DECONNEXION : Outil de Django 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # INSCRIPTION :
    path('register/', views.register_view, name='register'),

    path('profile/', views.profile_view, name='profile'),
]