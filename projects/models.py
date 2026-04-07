from django.db import models
from django.conf import settings

class Project(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom du projet")
    description = models.TextField(verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True)
    # On utilise 'created_by' au lieu de 'owner' pour correspondre à ta base Postgres
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='owned_projects'
    )

    def __str__(self):
        return self.name

class ProjectMember(models.Model):
    ROLE_CHOICES = [
        ('PM', 'Chef de Projet (PM)'),
        ('DEV', 'Développeur'),
        ('REQ', 'Demandeur'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='project_memberships')
    role = models.CharField(max_length=3, choices=ROLE_CHOICES, default='DEV')
    
    # AJOUTE CETTE LIGNE : Elle permet de gérer la colonne qui bloque dans Postgres
    joined_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        unique_together = ('project', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.project.name} ({self.get_role_display()})"