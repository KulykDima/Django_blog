from accounts.forms import MessageForm, UserRegisterForm
from accounts.models import User

from django.test import TestCase


class TestForms(TestCase):
    def setUp(self):
        self.username = 'Dima'
        self.password = 'Dimo4ka22222'
        self.email = 'Dima111@gmail.com'

    def test_register_form_valid_data(self):
        form = UserRegisterForm(
            data={
                'username': self.username,
                'email': self.email,
                'password1': self.password,
                'password2': self.password
            }
        )
        self.assertTrue(form.is_valid())

    def test_register_form_no_data(self):
        form = UserRegisterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)


class TestMessage(TestCase):
    username = None

    @classmethod
    def setUpTestData(cls):
        cls.username = 'user_1'

        User.objects.create(
            username=cls.username,
            password='1234qwerty',
            email='user_1@test.com',
            first_name='Dimitriy'
        )

    def setUp(self):
        self.user = User.objects.get(username=self.username)

    def test_new_message_form(self):
        form = MessageForm(
            data={
                'recipient': self.user.pk,
                'subject': self.user.email,
                'body': self.user.first_name
            }
        )
        self.assertTrue(form.is_valid())

    def test_message_form_no_data(self):
        form = MessageForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
