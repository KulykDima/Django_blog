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

    def test_blogger_view_url_resolves(self):
        url = reverse('accounts:bloggers_profile', kwargs={'pk': 1})

        self.assertEqual(resolve(url).func.view_class, BloggerProfileView)

    def test_incoming_message_view_url_resolves(self):
        url = reverse('accounts:message', kwargs={'pk': 1})

        self.assertEqual(resolve(url).func.view_class, IncomingMessage)

    def test_outgoing_message_view_url_resolves(self):
        url = reverse('accounts:out_message', kwargs={'pk': 1})

        self.assertEqual(resolve(url).func.view_class, OutgoingMessage)
