from django.db import models
from projects.models import Project, ProjectMember
from accounts.models import CustomUser
from sprints.models import Sprint

# Create your models here.

class Ticket(models.Model):
    TYPE_CHOICES = [
        ("BUG", "Bug"),
        ("FEATURE", "Feature"),
        ("TASK", "Tâche"),
    ]
    PRIORITY_CHOICES = [
        ("LOW", "Faible"),
        ("MEDIUM", "Moyenne"),
        ("HIGH", "Haute"),
    ]
    STATUS_CHOICES = [
        ("TODO", "To Do"),
        ("IN_PROGRESS", "In Progress"),
        ("REVIEW", "Review"),
        ("DONE", "Done"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tickets")
    reporter = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="reported_tickets")
    assignee = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tickets")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="TASK")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="MEDIUM")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="TODO")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    time_spent = models.PositiveIntegerField(default=0, verbose_name="Temps passé (heures)")
    sprint = models.ForeignKey(
        Sprint, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='tickets'
    )

class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class TicketTransitionHistory(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="transitions")
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)