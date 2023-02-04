from django.urls import path

from post.views import AddDislike, ListOfBloggers, blogger_details
from post.views import AddLike
from post.views import CreatePost
from post.views import PostDetail
from post.views import PostUpdate
from post.views import PostsList

app_name = 'posts'

urlpatterns = [
    path('', PostsList.as_view(), name='list'),
    path('createpost/', CreatePost.as_view(), name='create'),
    path('details/<uuid:uuid>', PostDetail.as_view(), name='detail'),
    path('<int:pk>/like/', AddLike.as_view(), name='like'),
    path('<int:pk>/dislike/', AddDislike.as_view(), name='dislike'),
    path('update/<uuid:uuid>', PostUpdate.as_view(), name='update'),
    path('bloggers/', ListOfBloggers.as_view(), name='blogger_list'),
    path('bloggers/blogger/<int:author_id>', blogger_details, name='blogger_detail'),
]
