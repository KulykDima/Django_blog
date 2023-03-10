from accounts.models import User

from django.test import TestCase

from post.models import Posts


class TestPosts(TestCase):
    posts = None
    username = None

    @classmethod
    def setUpTestData(cls):
        cls.username = 'user_1'

        User.objects.create(
            username=cls.username,
            password='1234qwerty',
            email='user_1@test.com',
            first_name='Dimitriy',
            is_activated=True
        )
        cls.posts = 'test_post'

        Posts.objects.create(
            title=cls.posts,
            author=User.objects.get(username=cls.username),
            text=str(123)
        )

    def test_uuid_label(self):
        post = Posts.objects.get(author__username=self.username)
        uuid = post._meta.get_field('uuid')

        self.assertEqual(uuid.db_index, uuid.unique, True)

    def test_author_label(self):
        post = Posts.objects.get(author__username=self.username)
        author = post._meta.get_field('author')

        self.assertEqual(author.null, author.blank, False)
        self.assertEqual(author.verbose_name, 'author')

    def test_other_labels(self):
        post = Posts.objects.get(author__username=self.username)
        like = post._meta.get_field('like')
        dislike = post._meta.get_field('dislike')
        create_date = post._meta.get_field('create_date')

        self.assertEqual(like.blank, dislike.blank, True)
        self.assertEqual(like.null, dislike.null, False)
        self.assertEqual(like.verbose_name, 'like')
        self.assertEqual(dislike.verbose_name, 'dislike')
        self.assertEqual(create_date.verbose_name, 'create date')
        self.assertEqual(create_date.blank, create_date.auto_now_add, True)
