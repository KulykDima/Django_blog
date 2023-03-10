from accounts.models import User

from django.test import TestCase, Client
from django.urls import reverse

from post.models import Posts


class TestPosts(TestCase):
    posts = None
    username = None

    @classmethod
    def setUpTestData(cls):
        cls.username = 'Dima'

        User.objects.create_user(
            username=cls.username,
            password='1234Qwerty',
            email='user_12@gmail.com',
            is_activated=True
        )
        cls.posts = 'test_post'

        Posts.objects.create(
            title=cls.posts,
            author=User.objects.get(username=cls.username),
            text=str(123)
        )

    def setUp(self):
        self.user = User.objects.get(username=self.username)
        self.post = Posts.objects.get(title=self.posts)
        self.client = Client()

    def test_list_view(self):
        response = self.client.get(reverse('posts:list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list_of_posts.html')

    def test_create_post_view(self):
        login = self.client.login(username='Dima', password='1234Qwerty')
        response = self.client.post(reverse('posts:create'))

        form_data = {'title': '123', 'author': self.user, 'text': '123'}
        index = reverse('posts:list')
        form_post_data = self.client.post((reverse('posts:create')), form_data)

        self.assertEqual(str(response.context['user']), str(self.user.username))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_post.html')
        self.assertRedirects(form_post_data, index, status_code=302, target_status_code=200)

    def test_post_detail_view(self):
        login = self.client.login(username='Dima', password='1234Qwerty')  # noqa
        response = self.client.get(reverse('posts:detail', kwargs={'uuid': self.post.uuid}))

        self.assertEqual(str(response.context['user']), str(self.user.username))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_details.html')

    def test_update_post_view(self):
        test_user1 = User.objects.create_user(username='user_1', password='Dimo4ka22222')
        test_user1.save()
        test_post = Posts.objects.create(author=test_user1, title='456', text='abc')
        test_post.save()

        login = self.client.login(username='Dima', password='1234Qwerty')  # noqa
        response = self.client.post(reverse('posts:update', kwargs={'uuid': self.post.uuid}))

        form_data = {'title': '120', 'text': '123'}
        form_post_data = self.client.post(reverse('posts:update',
                                                  kwargs={'uuid': self.post.uuid}), form_data)  # редактировать свой 200
        index = reverse('posts:detail', kwargs={'uuid': self.post.uuid})

        self.assertEqual(str(response.context['user']), str(self.user.username))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_post.html')
        self.assertRedirects(form_post_data, index, status_code=302, target_status_code=200)

        response_1 = self.client.get(reverse('posts:update',
                                             kwargs={'uuid': test_post.uuid}))  # редактировать пост автора user_1 (403)

        self.assertNotEqual(response_1.status_code, 200)

    def test_delete_post_view(self):
        test_user1 = User.objects.create_user(username='user_1', password='Dimo4ka22222')
        test_user1.save()
        test_post = Posts.objects.create(author=test_user1, title='456', text='abc')
        test_post.save()

        login = self.client.login(username='Dima', password='1234Qwerty')  # noqa
        response = self.client.post(reverse('posts:delete_post',
                                            kwargs={'uuid': self.post.uuid}))  # удалить свой пост (200)

        self.assertRedirects(response, reverse('posts:list'))

        response_1 = self.client.post(reverse('posts:delete_post',
                                              kwargs={'uuid': test_post.uuid}))  # удалить пост автора user_1 (302)

        self.assertNotEqual(response_1.status_code, 200)

    def test_bloggers_view(self):
        response = self.client.get(reverse('posts:blogger_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bloggers/bloggers_list.html')

    def test_bloggers_detail_view(self):
        login = self.client.login(username='Dima', password='1234Qwerty')   # noqa
        blogger = User.objects.get(username=self.user.username)
        response = self.client.get(reverse('posts:blogger_detail', kwargs={'pk': blogger.pk}))

        self.assertTemplateUsed(response, 'bloggers/blogger_details.html')
        self.assertEqual(str(response.context['user']), str(self.user.username))
        self.assertEqual(response.status_code, 200)

    def test_add_like_dislike_view(self):
        login = None
        login = self.client.login(username='Dima', password='1234Qwerty')   # noqa
        response_like = self.client.post(reverse('posts:like', kwargs={'pk': self.post.id}))
        response_dislike = self.client.post(reverse('posts:dislike', kwargs={'pk': self.post.id}))
        redirect_url = reverse('posts:list')

        self.assertEqual(response_like.status_code, response_dislike.status_code, 302)
        self.assertNotEqual(response_like.status_code, 200)
        self.assertNotEqual(response_dislike.status_code, 200)
        if login is None:
            self.assertRedirects(response_like, '/accounts/login/?next=/posts/1/like/',
                                 status_code=302, target_status_code=200)
        else:
            self.assertRedirects(response_like, redirect_url, status_code=302, target_status_code=200)
