from django import forms
from django.contrib.auth import get_user_model
from .models import ProjectMember

User = get_user_model()

class InviteMemberForm(forms.ModelForm):
    # On exclut les utilisateurs déjà membres du projet (optionnel pour l'instant)
    user = forms.ModelChoiceField(
        queryset=User.objects.all(), 
        label="Sélectionner un utilisateur",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    role = forms.ChoiceField(
        choices=ProjectMember.ROLE_CHOICES,
        label="Attribuer un rôle",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = ProjectMember
        fields = ['user', 'role']