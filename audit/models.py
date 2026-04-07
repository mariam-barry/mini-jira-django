from django.db import models
from django.conf import settings  # <--- Obligatoire pour utiliser settings.AUTH_USER_MODEL

class AuditLog(models.Model):
    # On utilise la chaîne 'tickets.Ticket' pour éviter les imports circulaires
    ticket = models.ForeignKey('tickets.Ticket', on_delete=models.CASCADE, related_name='audit_logs')
    
    # ON CHANGE 'auth.User' PAR settings.AUTH_USER_MODEL
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Modif sur {self.ticket.title} par {self.changed_by}"