from accounts.models import User

from django.core.signing import Signer
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

    def test_registration_valid(self):
        response = self.client.post(self.registration_url, self.data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.registration_done_url, status_code=302, target_status_code=200)
        self.assertEqual(response.url, self.registration_done_url)

        user = User.objects.first()
        self.assertEqual(user.username, self.data['username'])
        self.assertEqual(user.email, self.data['email'])
        self.assertTrue(user.check_password(self.data['password1']))
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_activated)

    def test_registration_invalid(self):
        self.data['password2'] = '123qwe!@'

        response = self.client.post(self.registration_url, self.data)
        self.assertNotEqual(response.status_code, 302)
        self.assertFalse(response.context['form'].is_valid())
        user = User.objects.filter(username=self.data['username'])
        self.assertEqual(len(user), 0)

    def test_activation_url(self):
        response = self.client.post(self.registration_url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.registration_done_url, status_code=302, target_status_code=200)

        user = User.objects.first()
        self.assertEqual(user.username, self.data['username'])

        signer = Signer()
        response = self.client.get(
            'http://localhost' + reverse('accounts:register_activate', kwargs={'sign': signer.sign(user.username)})
        )
        self.assertEqual(response.status_code, 200)

        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_activated)


class TestLogin(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='user_1', password='Dimo4ka201')
        test_user1.save()
        test_user2 = User.objects.create_user(username='user_2', password='Dimo4ka201')
        test_user2.save()

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='user_1', password='Dimo4ka201')
        response = self.client.get(reverse('index'))

        login_data = {'username': 'user_1', 'password': 'Dimo4ka201'}
        index = reverse('index')
        login_post_data = self.client.post((reverse('accounts:login')), login_data)

        self.assertEqual(str(response.context['user']), 'user_1')
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(login_post_data, index, status_code=302, target_status_code=200)

    def test_if_not_logged_in(self):
        blogger = User.objects.get(id=1)
        response_1 = self.client.get(reverse('accounts:profile'))
        response_2 = self.client.get(reverse('posts:blogger_detail', kwargs={'pk': blogger.pk}))

        self.assertRedirects(response_1, '/accounts/login/?next=%2Faccounts%2Fprofile%2F')
        self.assertRedirects(response_2, '/accounts/login/?next=%2Fposts%2Fbloggers%2Fblogger%2F1',
                             status_code=302,
                             target_status_code=200)


