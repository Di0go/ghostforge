# ghostforge/src/forge/forms.py
# 
# Forms for the attack and defense user input
# 
# <diogopinto> 2026+

from django import forms
from .models import AttackScenario, DefenseAnalysis

class AttackForm(forms.ModelForm):
    class Meta:
        model = AttackScenario
        fields = ['title', 'prompt', 'target_info']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ex: Phishing CEO Microsoft'
            }),
            'prompt': forms.Textarea(attrs={
                'rows': 4, 
                'class': 'form-control', 
                'placeholder': 'Ex: Write an email pretending to be the CEO asking for an urgent bank transfer.'
            }),
            'target_info': forms.Textarea(attrs={
                'rows': 3, 
                'class': 'form-control', 
                'placeholder': 'Ex: Target is John Doe, works in Finance, uses Outlook.'
            }),
        }
        labels = {
            'title': 'Scenario Name',
            'prompt': 'Attack Description',
            'target_info': 'Target Context (Optional)',
        }

class DefenseForm(forms.ModelForm):
    class Meta:
        model = DefenseAnalysis
        fields = ['input_file']
        widgets = {
            'input_file': forms.FileInput(attrs={'class': 'form-control form-control-lg'}),
        }
        labels = {
            'input_file': 'Upload Document (PDF)',
        }