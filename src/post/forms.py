from django import forms

import django_filters
from django.core.exceptions import ValidationError  # noqa
from django.db import models

from django_filters import FilterSet

from accounts.models import User
from .models import Comment
from .models import Posts


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = [
            'title',
            # 'author',
            'text',
        ]


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = [
            'title',
            'text',
        ]


class PostsFilterSet(FilterSet):
    class Meta:
        model = Posts
        fields = ['title', ]
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }


class BloggersFilterSet(FilterSet):
    class Meta:
        model = User
        fields = ['username', ]
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'body',
        )
