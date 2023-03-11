from accounts.models import User

from django.test import TestCase

from post.forms import CreatePostForm, UpdatePostForm
from post.models import Posts


class TestForms(TestCase):
    username = None
    posts = None

    @classmethod
    def setUpTestData(cls):
        cls.username = 'user_1'
        User.objects.create_user(
            username=cls.username,
            password='12345Qwerty',
            email='test1@gmail.com',
            is_activated=True
        )

        cls.posts = 'test_post'
        Posts.objects.create(
            title=cls.posts,
            author=User.objects.get(username=cls.username),
            text='abc123'
        )

    def setUp(self):
        self.post = Posts.objects.get(author__username=self.username)

    def test_create_update_post_form(self):
        form = CreatePostForm(
            data={
                'title': self.post.title,
                'text': self.post.text
            }
        )
        form_update = UpdatePostForm(
            data={
                'title': self.post.title,
                'text': self.post.text
            }
        )

        self.assertEqual(form.is_valid(), form_update.is_valid(), True)

    def test_create_post_no_data(self):
        form = CreatePostForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
