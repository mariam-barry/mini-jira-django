from django.core.exceptions import ValidationError
from django.db import transaction

# Imports depuis tes 5 applications
from .models import Ticket
from projects.models import ProjectMember
from audit.models import AuditLog  
from sprints.models import Sprint  

class TicketService:
    
    @staticmethod
    @transaction.atomic
    def create_ticket(project, reporter, data):
        """
        Création d'un ticket avec lien Sprint et premier log d'audit.
        """
        ticket = Ticket.objects.create(
            project=project,
            reporter=reporter,
            title=data['title'],
            description=data.get('description', ''),
            assignee=data.get('assignee'),
            type=data.get('type', 'TASK'),
            priority=data.get('priority', 'MEDIUM'),
            status='TODO',
            sprint=data.get('sprint') # On lie le ticket au sprint choisi
        )

        # Premier enregistrement dans l'historique (Audit)
        AuditLog.objects.create(
            ticket=ticket,
            old_status='NONE',
            new_status='TODO',
            changed_by=reporter
        )
        return ticket

    @staticmethod
    @transaction.atomic
    def update_ticket_status(ticket, new_status, user):
        """
        Gestion du Workflow strict + Enregistrement de l'audit.
        """
        old_status = ticket.status
        
        if old_status == new_status:
            return ticket

       
        if not ProjectMember.objects.filter(project=ticket.project, user=user).exists():
            raise ValidationError("Accès refusé : Vous n'êtes pas membre de ce projet.")

        
        if old_status == 'DONE' and new_status != 'TODO':
            raise ValidationError("Ce ticket est terminé. Repassez-le en 'To Do' pour le modifier.")

       
        allowed = {
            'TODO': ['IN_PROGRESS'],
            'IN_PROGRESS': ['REVIEW', 'TODO'],
            'REVIEW': ['DONE', 'IN_PROGRESS'],
            'DONE': ['TODO'],
        }

        if new_status not in allowed.get(old_status, []):
            raise ValidationError(f"Transition impossible de {old_status} vers {new_status}.")

        
        ticket.status = new_status
        ticket.save()

        AuditLog.objects.create(
            ticket=ticket,
            old_status=old_status,
            new_status=new_status,
            changed_by=user
        )
        
        return ticket