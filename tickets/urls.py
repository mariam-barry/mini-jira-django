from django.urls import path
from . import views

urlpatterns = [
    path('project/<int:project_id>/', views.ticket_list, name='ticket_list'), 
    path('project/<int:project_id>/create/', views.create_ticket, name='create_ticket'),
    path('<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('<int:ticket_id>/update-status/', views.update_status, name='update_status'),
    path('<int:ticket_id>/log-time/', views.log_time, name='log_time'),
    
]