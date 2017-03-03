from django import forms
from .models import Project, Comment, CommentSecondLevel, ContactUsModel


class StartProjectForm(forms.ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    success_url = '/app/'

    class Meta:
        model = Project
        exclude = ['when']
        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'query': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'file': forms.FileInput(attrs={'class': 'upload'}),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ['is_moderated', 'blog']

        widgets = {
            'author_name': forms.TextInput(attrs={'class': 'form-control'}),
            'author_email': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }


class SecondLevelCommentForm(forms.ModelForm):

    class Meta:
        model = CommentSecondLevel
        exclude = ['is_moderated', 'father_comment']
        widgets = {
            'author_name': forms.TextInput(attrs={'class': 'form-control'}),
            'author_email': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }


class ContactUsForm(forms.ModelForm):

    class Meta:
        model = ContactUsModel
        fields = ['author_name', 'author_email', 'message']
        widgets = {
            'author_name': forms.TextInput(attrs={'class': 'form-control'}),
            'author_email': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': '7'}),
        }
