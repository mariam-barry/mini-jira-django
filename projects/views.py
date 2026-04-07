from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project, ProjectMember
from .forms import InviteMemberForm
from .services import ProjectService
from tickets.models import Ticket

@login_required
def project_list(request):
    # On récupère les participations de l'utilisateur pour voir ses rôles
    memberships = ProjectMember.objects.filter(user=request.user).select_related('project')
    return render(request, 'projects/project_list.html', {'memberships': memberships})

@login_required
def invite_member(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    # Sécurité : Seul le PM peut inviter
    if not ProjectService.is_pm(request.user, project):
        return render(request, '403.html', {'message': "Accès refusé : Vous n'êtes pas PM."}, status=403)

    if request.method == "POST":
        form = InviteMemberForm(request.POST)
        if form.is_valid():
            new_member = form.save(commit=False)
            new_member.project = project
            new_member.save()
            return redirect('project_list')
    else:
        form = InviteMemberForm()
    
    return render(request, 'projects/invite_member.html', {
        'form': form, 
        'project': project
    })

@login_required
def project_board(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    # On récupère tous les tickets du projet
    all_tickets = Ticket.objects.filter(project=project)
    
    # Utilisation de noms de clés plus propres pour l'affichage des colonnes
    kanban_data = {
        'À Faire (To Do)': all_tickets.filter(status='TODO'),
        'En Cours (In Progress)': all_tickets.filter(status='IN_PROGRESS'),
        'Révision (Review)': all_tickets.filter(status='REVIEW'),
        'Terminé (Done)': all_tickets.filter(status='DONE'),
    }
    
    return render(request, 'projects/board.html', {
        'project': project,
        'kanban': kanban_data
    })