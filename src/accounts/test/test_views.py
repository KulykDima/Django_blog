from accounts.models import Message, User

from django.test import Client
from django.test import TestCase
from django.urls import reverse


class TestViews(TestCase):
    def setUp(self):
        self.data = {
            'username': 'user_1',
            'password1': '123Qwe!@#',
            'password2': '123Qwe!@#',
            'email': 'user_1@gmail.com'
        }
        self.client = Client()
        self.registration_url = reverse('accounts:register')
        self.registration_done_url = reverse('accounts:register_done')

    def test_index_loads_properly(self):
        response = self.client.get('http://127.0.0.1:12345')

        self.assertEqual(response.status_code, 200)

    def test_registration_invalid(self):
        self.data['password2'] = '123qwe!@'

        response = self.client.post(self.registration_url, self.data)
        self.assertNotEqual(response.status_code, 302)
        self.assertFalse(response.context['form'].is_valid())
        user = User.objects.filter(username=self.data['username'])
        self.assertEqual(len(user), 0)


class TestLogin(TestCase):
    test_user1 = None
    test_user2 = None
    test_message = None

    @classmethod
    def setUpTestData(cls):
        cls.test_user1 = 'user_1'
        User.objects.create_user(
            username=cls.test_user1,
            password='Dimo4ka22222',
            email='user_1@test.com',
            first_name='Dimitriy',
            is_activated=True
        )

        cls.test_user2 = 'user_2'
        User.objects.create_user(
            username=cls.test_user2,
            password='Dimo4ka22222',
            email='user_2@test.com',
            first_name='user_2',
            is_activated=True
        )

        # cls.message = 'Subject'
        Message.objects.create(
            sender=User.objects.get(username=cls.test_user1),
            recipient=User.objects.get(username=cls.test_user2),
            subject='Subject',
            body='123'
        )

    def setUp(self):
        self.message = Message.objects.get(sender=User.objects.get(username=self.test_user1))
        self.client = Client()

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='user_1', password='Dimo4ka22222')    # noqa
        response = self.client.get(reverse('index'))

        login_data = {'username': 'user_1', 'password': 'Dimo4ka22222'}
        index = reverse('index')
        login_post_data = self.client.post((reverse('accounts:login')), login_data)

        self.assertEqual(str(response.context['user']), 'user_1')
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(login_post_data, index, status_code=302, target_status_code=200)

    def test_if_not_logged_in(self):
        blogger = User.objects.get(username=self.test_user1)
        response_1 = self.client.get(reverse('accounts:profile'))
        response_2 = self.client.get(reverse('posts:blogger_detail', kwargs={'pk': blogger.pk}))
        response_3 = self.client.get(reverse('accounts:inbox'))

        self.assertRedirects(response_1, '/accounts/login/?next=%2Faccounts%2Fprofile%2F')
        self.assertRedirects(response_2, '/accounts/login/?next=/posts/bloggers/blogger/1',
                             status_code=302,
                             target_status_code=200)
        self.assertRedirects(response_3, '/accounts/login/?next=/accounts/profile/inbox',
                             status_code=302,
                             target_status_code=200)

    def test_delete_message(self):
        login = self.client.login(username='user_1', password='Dimo4ka22222')    # noqa
        response = self.client.post(reverse('accounts:delete_message', kwargs={'id': self.message.id}))
        inbox = reverse('accounts:inbox')

        self.assertRedirects(response, inbox, status_code=302, target_status_code=200)

    def test_logout_uses_correct_template(self):
        login = self.client.login(username='user_1', password='Dimo4ka22222')  # noqa
        logout = self.client.post(reverse('accounts:logout'))

        self.assertEqual(logout.status_code, 200)
