from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView

from post.forms import CreatePostForm
from post.models import Posts


class PostsList(ListView):
    model = Posts
    template_name = 'list_of_posts.html'


class CreatePost(LoginRequiredMixin, CreateView):
    model = Posts
    template_name = 'create_post.html'
    form_class = CreatePostForm
    success_url = reverse_lazy('posts:list')

