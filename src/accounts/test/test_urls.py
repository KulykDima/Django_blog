from accounts.models import Message, User
from accounts.views import BloggerProfileView
from accounts.views import CreateNewMessage
from accounts.views import Inbox
from accounts.views import IncomingMessage
from accounts.views import Outbox
from accounts.views import OutgoingMessage
from accounts.views import UserProfile
from accounts.views import UserRegistrationView
from accounts.views import UserUpdateView

from django.test import SimpleTestCase, TestCase
from django.urls import resolve
from django.urls import reverse


class TestUrls(SimpleTestCase):
    def test_register_url_resolves(self):
        url = reverse('accounts:register')
        self.assertEqual(resolve(url).func.view_class, UserRegistrationView)

    def test_profile_url_resolves(self):
        url = reverse('accounts:profile')
        self.assertEqual(resolve(url).func.view_class, UserProfile)

    def test_inbox_url_resolves(self):
        url = reverse('accounts:inbox')
        self.assertEqual(resolve(url).func.view_class, Inbox)

    def test_outbox_url_resolves(self):
        url = reverse('accounts:outbox')
        self.assertEqual(resolve(url).func.view_class, Outbox)

    def test_profile_update_url_resolves(self):
        url = reverse('accounts:profile_update')
        self.assertEqual(resolve(url).func.view_class, UserUpdateView)

    def test_create_message_url_resolves(self):
        url = reverse('accounts:create_message')
        self.assertEqual(resolve(url).func.view_class, CreateNewMessage)


class TestUrlsWithKwargs(TestCase):
    username = None

    @classmethod
    def setUpTestData(cls):
        cls.username = 'user_1'

        User.objects.create(
            username=cls.username,
            password='1234Qwerty',
            email='user_1@test.com',
            first_name='Dimitriy',
            is_activated=True
        )

    def setUp(self):
        self.user = User.objects.get(username=self.username)
        self.incoming_message = Message.objects.create(
            sender=self.user,
            recipient=self.user,
            subject='123',
            body='123'
        )

    def test_blogger_view_url_resolves(self):
        url = reverse('accounts:bloggers_profile', kwargs={'pk': self.user.pk})

        self.assertEqual(resolve(url).func.view_class, BloggerProfileView)

    def test_incoming_message_view_url_resolves(self):
        url = reverse('accounts:message', kwargs={'pk': self.incoming_message.pk})

        self.assertEqual(resolve(url).func.view_class, IncomingMessage)

    def test_outgoing_message_view_url_resolves(self):
        url = reverse('accounts:out_message', kwargs={'pk': self.incoming_message.pk})

        self.assertEqual(resolve(url).func.view_class, OutgoingMessage)
