from django.contrib import admin
from .models import Project, ProjectMember

class ProjectMemberInline(admin.TabularInline):
    model = ProjectMember
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    # Changement de 'owner' en 'created_by' pour correspondre au modèle
    list_display = ('name', 'created_by', 'created_at') 
    inlines = [ProjectMemberInline]

@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'role')
    list_filter = ('project', 'role')