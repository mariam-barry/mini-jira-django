from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Les rôles globaux de l'utilisateur sur la plateforme
    ROLE_CHOICES = [
        ("ADMIN", "Admin"),
        ("PM", "Chef de projet"),
        ("DEV", "Développeur"),
        ("REQUESTER", "Demandeur"),
    ]
    
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default="REQUESTER",
        verbose_name="Rôle Global"
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"