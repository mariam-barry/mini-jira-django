from django import forms
from django.contrib.auth import get_user_model
from .models import Ticket, TicketComment
from projects.models import ProjectMember

User = get_user_model()

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "type", "priority", "assignee"]

    def __init__(self, *args, **kwargs):
        # On récupère le projet passé par la vue
        project = kwargs.pop("project", None)
        super().__init__(*args, **kwargs)
        
        if project:
            # On récupère les IDs des utilisateurs qui sont membres de ce projet
            user_ids = ProjectMember.objects.filter(project=project).values_list('user_id', flat=True)
            
            # On donne au champ 'assignee' un QUERYSET d'utilisateurs (très important !)
            self.fields["assignee"].queryset = User.objects.filter(id__in=user_ids)

class TicketCommentForm(forms.ModelForm):
    class Meta:
        model = TicketComment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={
                "rows": 3, 
                "placeholder": "Votre commentaire...",
                "style": "width: 100%; border-radius: 5px; border: 1px solid #ccc;"
            })
        }

class TimeLogForm(forms.Form):
    hours = forms.IntegerField(
        min_value=1, 
        label="Ajouter des heures",
        widget=forms.NumberInput(attrs={'style': 'width: 80px; padding: 5px; border-radius: 4px; border: 1px solid #ccc;'})
    )