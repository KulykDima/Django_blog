from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render  # noqa
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView


from post.forms import CreatePostForm
from post.forms import PostsFilterSet
from post.forms import UpdatePostForm
from post.models import Posts


class PostsList(ListView):
    model = Posts
    template_name = 'list_of_posts.html'

    def get_queryset(self):
        posts = Posts.objects.all()
        filter_form = PostsFilterSet(data=self.request.GET, queryset=posts)

        return filter_form


class CreatePost(LoginRequiredMixin, CreateView):
    model = Posts
    template_name = 'create_post.html'
    form_class = CreatePostForm
    success_url = reverse_lazy('posts:list')


class PostDetail(DetailView):
    model = Posts
    template_name = 'post_details.html'
    pk_url_kwarg = 'uuid'

    def get_object(self, queryset=None):
        uuid = self.kwargs.get('uuid')
        return self.model.objects.get(uuid=uuid)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(object_list=self.get_queryset(), **kwargs)
        context['likeusers'] = self.get_object().like.prefetch_related('likes__like')
        context['dislikeusers'] = self.get_object().dislike.prefetch_related('dislikes__dislike')
        print(context)
        return context


class AddLike(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):
        post = Posts.objects.get(pk=pk)

        is_dislike = False

        for dislike in post.dislike.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            post.dislike.remove(request.user)

        is_like = False

        for like in post.like.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.like.add(request.user)

        if is_like:
            post.like.remove(request.user)

        return HttpResponseRedirect(reverse('posts:list'))


class AddDislike(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):
        post = Posts.objects.get(pk=pk)

        is_like = False

        for like in post.like.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            post.like.remove(request.user)

        is_dislike = False

        for dislike in post.dislike.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            post.dislike.add(request.user)

        if is_dislike:
            post.dislike.remove(request.user)

        return HttpResponseRedirect(reverse('posts:list'))


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Posts
    form_class = UpdatePostForm
    template_name = 'update_post.html'

    def get_object(self, queryset=None):
        uuid = self.kwargs.get('uuid')
        return self.model.objects.get(uuid=uuid)

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        uuid = self.kwargs.get('uuid')

        return (
            reverse(
                'posts:detail',
                kwargs={
                    'uuid': uuid,
                }
            )
        )
