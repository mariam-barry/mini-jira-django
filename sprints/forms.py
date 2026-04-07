from django import forms
from .models import Sprint

class SprintForm(forms.ModelForm): # Correction ici : juste forms.ModelForm
    class Meta:
        model = Sprint
        fields = ['name', 'start_date', 'end_date', 'goal']
        
        # On ajoute des classes Bootstrap pour que ce soit joli
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Sprint 1'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'goal': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        # Règle métier : cohérence des dates
        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError("La date de fin ne peut pas être avant la date de début.")
        
        return cleaned_data