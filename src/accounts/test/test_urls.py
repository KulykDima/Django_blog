from accounts.views import UserRegistrationView, Inbox, Outbox
from accounts.views import UserProfile

from django.test import SimpleTestCase
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
