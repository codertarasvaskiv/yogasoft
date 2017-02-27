from django import forms
from .models import Project, Comment


class StartProjectForm(forms.ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    success_url = '/app/'

    class Meta:
        model = Project
        exclude = ['when']

