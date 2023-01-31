from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404  # noqa
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic.list import MultipleObjectMixin

from post.forms import CommentForm
from post.forms import CreatePostForm
from post.forms import PostsFilterSet
from post.forms import UpdatePostForm
from post.models import Posts


class PostsList(ListView):
    model = Posts
    template_name = 'list_of_posts.html'
    paginate_by = 3

    def get_filter(self):
        posts = Posts.objects.all()
        filter_form = PostsFilterSet(data=self.request.GET, queryset=posts)

        return filter_form

    def get_queryset(self):
        return self.get_filter().qs


class CreatePost(LoginRequiredMixin, CreateView):
    model = Posts
    template_name = 'create_post.html'
    form_class = CreatePostForm
    success_url = reverse_lazy('posts:list')


class PostDetail(LoginRequiredMixin, DetailView, MultipleObjectMixin):
    model = Posts
    template_name = 'post_details.html'
    pk_url_kwarg = 'uuid'
    paginate_by = 2

    def get_object(self, queryset=None):
        uuid = self.kwargs.get('uuid')
        return self.model.objects.get(uuid=uuid)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(object_list=self.get_queryset(), **kwargs)
        page = self.request.GET.get('page')
        context['likeusers'] = self.get_object().like.prefetch_related('likes__like')
        context['dislikeusers'] = self.get_object().dislike.prefetch_related('dislikes__dislike')
        context['comments'] = self.get_object().comments.prefetch_related('post').order_by('-created')
        context['comments'] = Paginator(context['comments'], 4).get_page(page)
        print(context)
        return context

    def post(self, request, uuid, *args, **kwargs):
        post = Posts.objects.get(uuid=uuid)
        comments = post.comments.filter(active=True)

        if request.method == 'POST':
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.user = self.request.user
                new_comment.post = post
                new_comment.save()
        else:
            comment_form = CommentForm()

        return render(request,
                      'post_details.html',
                      {'posts': post, 'comments': comments, 'comment_form': comment_form})


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
