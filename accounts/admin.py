from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.



class CustomUserAdmin(UserAdmin):
    # 1. On définit les colonnes à afficher dans la liste des utilisateurs
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    
    # 2. On ajoute le champ 'role' dans les formulaires de modification (Edit)
    fieldsets = UserAdmin.fieldsets + (
        ('Informations de rôle', {'fields': ('role',)}),
    )
    
    # 3. On ajoute le champ 'role' dans le formulaire de création (Add)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations de rôle', {'fields': ('role',)}),
    )

# On enregistre le modèle avec sa configuration personnalisée
admin.site.register(CustomUser, CustomUserAdmin)