from django import forms
from .models import *
from django.contrib.auth.models import User


class StartProjectForm(forms.ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    success_url = '/app/'

    class Meta:
        model = Project
        exclude = ['when', 'is_opened']
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


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password',)


class YogaUserForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    class Meta:
        model = UserYoga
        fields = ('extra_data',)


class CreateBlogForm(forms.ModelForm):

    class Meta:
        model = BlogPost
        exclude = ["author", "date"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'nameUA': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': '7'}),
            'textUA': forms.Textarea(attrs={'class': 'form-control', 'rows': '7'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class CreatePortfolio(forms.ModelForm):

    class Meta:
        model = PortfolioContent
        exclude = []
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '7'}),
            'nameUA': forms.TextInput(attrs={'class': 'form-control'}),
            'descriptionUA': forms.Textarea(attrs={'class': 'form-control', 'rows': '7'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            "technologies": forms.TextInput(attrs={'class': 'form-control'}),
            'link': forms.TextInput(attrs={'class': 'form-control'}),
            'client': forms.TextInput(attrs={'class': 'form-control'}),
        }
