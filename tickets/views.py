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
    project = get_object_or_404(Project, id=project_id)
    tickets = Ticket.objects.filter(project=project).select_related('assignee', 'reporter')

    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')
    assignee_filter = request.GET.get('assignee')

    if status_filter:
        tickets = tickets.filter(status=status_filter)
    if priority_filter:
        tickets = tickets.filter(priority=priority_filter)
    if assignee_filter:
        tickets = tickets.filter(assignee_id=assignee_filter)

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
    project = get_object_or_404(Project, id=project_id)
   
   
    if request.user.role not in ['REQ', 'REQUESTER', 'Demandeur', 'PM']:
        messages.error(request, "Seul le Demandeur ou le PM peut créer un ticket.")
        return redirect('project_board', project_id=project.id)
    
    if request.method == 'POST':
        form = TicketForm(request.POST, project=project)
        if form.is_valid():
            try:
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
        
    return render(request, 'tickets/ticket_form.html', {'form': form, 'project': project})

@login_required
def ticket_detail(request, ticket_id):
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
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    
    roles_autorises = ['DEV', 'DEVELOPER', 'Développeur', 'PM']
    if request.user.role not in roles_autorises:
        messages.error(request, f"Rôle '{request.user.role}' non autorisé à modifier le statut.")
        return redirect('ticket_detail', ticket_id=ticket.id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        try:
            TicketService.update_ticket_status(ticket, new_status, request.user)
            messages.success(request, f"Statut mis à jour : {ticket.get_status_display()}")
        except ValidationError as e:
            messages.error(request, e.message)
            
    return redirect('ticket_detail', ticket_id=ticket.id)

@login_required
def log_time(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    
    if request.user.role not in ['DEV', 'DEVELOPER', 'Développeur']:
        messages.error(request, "Action réservée aux Développeurs.")
        return redirect('ticket_detail', ticket_id=ticket.id)

    if request.method == "POST":
        hours = request.POST.get('hours')
        if hours:
            try:
                ticket.time_spent += float(hours)
                ticket.save()
                messages.success(request, f"{hours}h ajoutées au compteur.")
            except ValueError:
                messages.error(request, "Veuillez entrer un nombre valide.")
            
    return redirect('ticket_detail', ticket_id=ticket.id)