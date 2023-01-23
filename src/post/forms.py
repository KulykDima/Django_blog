from django import forms
from django.core.exceptions import ValidationError

from .models import Posts


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = [
            'title',
            'author',
            'text',
        ]


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = [
            'title',
            'text',
        ]
