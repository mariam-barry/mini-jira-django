from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('<int:project_id>/invite/', views.invite_member, name='invite_member'),
    path('<int:project_id>/board/', views.project_board, name='project_board'),
   
]