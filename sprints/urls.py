from django.urls import path
from . import views

urlpatterns = [
    # Liste des sprints d'un projet
    path('project/<int:project_id>/', views.sprint_list, name='sprint_list'),
    
    # Création d'un sprint (Réservé au PM)
    path('project/<int:project_id>/create/', views.create_sprint, name='create_sprint'),
    
    # Ajouter un ticket à un sprint (Planning)
    path('<int:sprint_id>/add-ticket/', views.add_ticket_to_sprint, name='add_ticket_to_sprint'),
    
    # Clôturer un sprint (Réservé au PM)
    path('<int:sprint_id>/close/', views.close_sprint, name='close_sprint'),
]