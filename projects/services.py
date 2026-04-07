from .models import ProjectMember

class ProjectService:
    @staticmethod
    def is_pm(user, project):
        """Vérifie si l'utilisateur est Chef de Projet sur ce projet."""
        return ProjectMember.objects.filter(
            project=project, 
            user=user, 
            role='PM'
        ).exists()

    @staticmethod
    def get_user_role(user, project):
        """Récupère le rôle d'un utilisateur dans un projet donné."""
        member = ProjectMember.objects.filter(user=user, project=project).first()
        return member.role if member else None