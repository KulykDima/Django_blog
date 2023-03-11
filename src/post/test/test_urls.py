from accounts.models import User

from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse

from post.models import Posts
from post.views import BloggerDetails
from post.views import CreatePost
from post.views import DeletePost
from post.views import ListOfBloggers
from post.views import PostDetail
from post.views import PostUpdate
from post.views import PostsList


class TestUrls(SimpleTestCase):

    def test_post_list_resolves(self):
        url = reverse('posts:list')

        self.assertEqual(resolve(url).func.view_class, PostsList)

    def test_bloggers_list_resolves(self):
        url = reverse('posts:blogger_list')

        self.assertEqual(resolve(url).func.view_class, ListOfBloggers)

    def test_create_post_resolves(self):
        url = reverse('posts:create')

        self.assertEqual(resolve(url).func.view_class, CreatePost)


class TestPostUrlsWithKwargs(TestCase):
    posts = None
    username = None

    @classmethod
    def setUpTestData(cls):
        cls.username = 'user_1'
        User.objects.create_user(
            username=cls.username,
            email='Dima1@gmail.com',
            password='1234Qwerty',
            is_activated=True
        )

        cls.posts = 'test_post'
        Posts.objects.create(
            title=cls.posts,
            author=User.objects.get(username=cls.username),
            text='123abc'
        )

    def test_post_detail_resolves(self):
        post = Posts.objects.get(title=self.posts)
        url = reverse('posts:detail', kwargs={'uuid': post.uuid})

        self.assertEqual(resolve(url).func.view_class, PostDetail)

    def test_blogger_detail_resolves(self):
        user = User.objects.get(username=self.username)
        url = reverse('posts:blogger_detail', kwargs={'pk': user.pk})

        self.assertEqual(resolve(url).func.view_class, BloggerDetails)

    def test_update_post_resolves(self):
        post = Posts.objects.get(title=self.posts)
        url = reverse('posts:update', kwargs={'uuid': post.uuid})

        self.assertEqual(resolve(url).func.view_class, PostUpdate)

    def test_delete_post_resolves(self):
        post = Posts.objects.get(title=self.posts)
        url = reverse('posts:delete_post', kwargs={'uuid': post.uuid})

        self.assertEqual(resolve(url).func.view_class, DeletePost)
