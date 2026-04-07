from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Sprint
from .forms import SprintForm
from projects.models import Project
from tickets.models import Ticket

@login_required
def sprint_list(request, project_id):
    """Affiche tous les sprints d'un projet."""
    project = get_object_or_404(Project, id=project_id)
    sprints = Sprint.objects.filter(project=project).order_by('-start_date')
    return render(request, 'sprints/sprint_list.html', {
        'project': project,
        'sprints': sprints
    })

@login_required
def create_sprint(request, project_id):
    """
    RÈGLE : Seul le PM peut créer un Sprint (Point 2).
    """
    project = get_object_or_404(Project, id=project_id)

    # Sécurité : Vérification du rôle PM
    if request.user.role != 'PM':
        messages.error(request, "Accès refusé : Seul le Chef de Projet (PM) peut créer un Sprint.")
        return redirect('project_board', project_id=project.id)

    if request.method == 'POST':
        form = SprintForm(request.POST)
        if form.is_valid():
            sprint = form.save(commit=False)
            sprint.project = project
            sprint.save()
            messages.success(request, f"Sprint '{sprint.name}' créé avec succès.")
            return redirect('sprint_list', project_id=project.id)
    else:
        form = SprintForm()

    return render(request, 'sprints/sprint_form.html', {
        'form': form,
        'project': project
    })

@login_required
def add_ticket_to_sprint(request, sprint_id):
    """
    RÈGLE : Le PM planifie le sprint (Point 2 & 7).
    """
    sprint = get_object_or_404(Sprint, id=sprint_id)
    
    if request.user.role != 'PM':
        messages.error(request, "Seul le PM peut planifier les tickets dans un sprint.")
        return redirect('project_board', project_id=sprint.project.id)

    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')
        ticket = get_object_or_404(Ticket, id=ticket_id, project=sprint.project)
        
        ticket.sprint = sprint
        ticket.save()
        messages.success(request, f"Ticket {ticket.title} ajouté au sprint.")
        
    return redirect('sprint_detail', sprint_id=sprint.id)

@login_required
def close_sprint(request, sprint_id):
    """
    RÈGLE : "PM : valide la clôture" (Point 2).
    """
    sprint = get_object_or_404(Sprint, id=sprint_id)
    
    if request.user.role != 'PM':
        messages.error(request, "Seul le PM peut clôturer un sprint.")
        return redirect('project_board', project_id=sprint.project.id)

    sprint.active = False # Ou changer un statut 'CLOSED'
    sprint.save()
    messages.success(request, f"Le sprint {sprint.name} est maintenant terminé.")
    return redirect('sprint_list', project_id=sprint.project.id)
