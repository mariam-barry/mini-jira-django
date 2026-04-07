from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from .models import Ticket, TicketComment
from .forms import TicketForm, TicketCommentForm
from .services import TicketService
from projects.models import Project, ProjectMember

User = get_user_model()

@login_required
def ticket_list(request, project_id):
    """
    Écran : Liste tickets (Point 5)
    Affiche les tickets d'un projet avec filtres.
    """
    project = get_object_or_404(Project, id=project_id)
    tickets = Ticket.objects.filter(project=project).select_related('assignee', 'reporter')

    # Récupération des filtres depuis l'URL
    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')
    assignee_filter = request.GET.get('assignee')

    if status_filter:
        tickets = tickets.filter(status=status_filter)
    if priority_filter:
        tickets = tickets.filter(priority=priority_filter)
    if assignee_filter:
        tickets = tickets.filter(assignee_id=assignee_filter)

    # Pour le menu déroulant des membres dans le filtre
    members = User.objects.filter(project_memberships__project=project)

    return render(request, 'tickets/ticket_list.html', {
        'project': project,
        'tickets': tickets,
        'status_choices': Ticket.STATUS_CHOICES,
        'priority_choices': Ticket.PRIORITY_CHOICES,
        'members': members,
    })

@login_required
def create_ticket(request, project_id):
    """
    Écran : Création de ticket (Point 5)
    """
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        form = TicketForm(request.POST, project=project)
        if form.is_valid():
            try:
                # On utilise le service pour garantir les règles métier
                TicketService.create_ticket(
                    project=project, 
                    reporter=request.user, 
                    data=form.cleaned_data
                )
                messages.success(request, "Ticket créé avec succès.")
                return redirect('project_board', project_id=project.id)
            except ValidationError as e:
                form.add_error(None, e.message)
    else:
        form = TicketForm(project=project)
        
    return render(request, 'tickets/ticket_form.html', {
        'form': form, 
        'project': project
    })

@login_required
def ticket_detail(request, ticket_id):
    """
    Écran : Détail ticket (Point 5)
    Gère aussi l'ajout de commentaires (Point 3).
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    comments = ticket.comments.all().order_by('-created_at')
    
    if request.method == 'POST':
        comment_form = TicketCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.ticket = ticket
            comment.author = request.user
            comment.save()
            messages.success(request, "Commentaire ajouté.")
            return redirect('ticket_detail', ticket_id=ticket.id)
    else:
        comment_form = TicketCommentForm()
        
    return render(request, 'tickets/ticket_detail.html', {
        'ticket': ticket,
        'comments': comments,
        'comment_form': comment_form,
        'status_choices': Ticket.STATUS_CHOICES,
    })

@login_required
def update_status(request, ticket_id):
    """
    Action : Workflow (Point 4)
    Met à jour le statut via le Service.
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        try:
            # Appel au service pour gérer la logique de transition
            TicketService.update_ticket_status(ticket, new_status, request.user)
            messages.success(request, f"Statut mis à jour vers {ticket.get_status_display()}.")
        except ValidationError as e:
            messages.error(request, e.message)
            
    return redirect('ticket_detail', ticket_id=ticket.id)



@login_required
def log_time(request, ticket_id):
    if request.method == "POST":
        ticket = get_object_or_404(Ticket, id=ticket_id)
        # On récupère la valeur envoyée par le formulaire
        hours_to_add = request.POST.get('hours')
        
        if hours_to_add and int(hours_to_add) > 0:
            ticket.time_spent += int(hours_to_add)
            ticket.save()
            messages.success(request, f"{hours_to_add} heures ajoutées au ticket.")
        
        return redirect('ticket_detail', ticket_id=ticket.id)
    return redirect('project_list')