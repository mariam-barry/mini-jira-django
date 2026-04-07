from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, ProjectMember
from .forms import InviteMemberForm
from .services import ProjectService
from tickets.models import Ticket


@login_required
def project_list(request):
    """
    Tout le monde peut voir la liste des projets auxquels il appartient.
    """
    memberships = ProjectMember.objects.filter(user=request.user).select_related('project')
    return render(request, 'projects/project_list.html', {'memberships': memberships})

@login_required
def invite_member(request, project_id):
    """
    RÈGLE : Seul le Chef de projet (PM) ou l'Admin peut affecter/inviter des membres.
    """
    project = get_object_or_404(Project, id=project_id)
    
    # Vérification stricte du rôle PM (via ton service ou le champ role)
    if request.user.role != 'PM' and not request.user.is_staff:
        messages.error(request, "Accès refusé : Seul le PM peut inviter des membres au projet.")
        return redirect('project_board', project_id=project.id)

    if request.method == "POST":
        form = InviteMemberForm(request.POST)
        if form.is_valid():
            new_member = form.save(commit=False)
            new_member.project = project
            new_member.save()
            messages.success(request, f"Membre ajouté au projet {project.name}.")
            return redirect('project_board', project_id=project.id)
    else:
        form = InviteMemberForm()
    
    return render(request, 'projects/invite_member.html', {
        'form': form, 
        'project': project
    })

@login_required
def project_board(request, project_id):
    """
    Tout le monde peut suivre l'avancement (Point 2: Demandeur suit l'avancement).
    """
    project = get_object_or_404(Project, id=project_id)
    
    all_tickets = Ticket.objects.filter(project=project)
    
    kanban_data = {
        'TODO': all_tickets.filter(status='TODO'),
        'IN_PROGRESS': all_tickets.filter(status='IN_PROGRESS'),
        'REVIEW': all_tickets.filter(status='REVIEW'),
        'DONE': all_tickets.filter(status='DONE'),
    }
    
    return render(request, 'projects/board.html', {
        'project': project,
        'kanban': kanban_data
    })