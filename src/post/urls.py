from django.urls import path

from post.views import AddDislike
from post.views import AddLike
from post.views import BloggerDetails
from post.views import CreatePost
from post.views import DeletePost
from post.views import ListOfBloggers
from post.views import PersonalBloggerPostsList
from post.views import PostDetail
from post.views import PostUpdate
from post.views import PostsList

app_name = 'posts'

urlpatterns = [
    path('', PostsList.as_view(), name='list'),
    path('createpost/', CreatePost.as_view(), name='create'),
    path('details/<uuid:uuid>', PostDetail.as_view(), name='detail'),
    path('delete/<uuid:uuid>', DeletePost.as_view(), name='delete_post'),
    path('<int:pk>/like/', AddLike.as_view(), name='like'),
    path('<int:pk>/dislike/', AddDislike.as_view(), name='dislike'),
    path('update/<uuid:uuid>', PostUpdate.as_view(), name='update'),
    path('bloggers/', ListOfBloggers.as_view(), name='blogger_list'),
    path('bloggers/blogger/<int:pk>', BloggerDetails.as_view(), name='blogger_detail'),
    path('blogger/post_list/', PersonalBloggerPostsList.as_view(), name='personal_blog'),
]
