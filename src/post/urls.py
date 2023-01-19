from django.urls import path

from post.views import CreatePost
from post.views import PostsList

app_name = 'posts'

urlpatterns = [
    path('', PostsList.as_view(), name='list'),
    path('createpost/', CreatePost.as_view(), name='create'),
]
