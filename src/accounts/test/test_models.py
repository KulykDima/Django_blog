from accounts.models import Message, User

from django.test import TestCase


class TestModels(TestCase):
    username = None

    @classmethod
    def setUpTestData(cls):
        cls.username = 'user_1'

        User.objects.create(
            username=cls.username,
            password='1234qwerty',
            email='user_1@test.com',
            first_name='Dimitriy',
            is_activated=True,
            is_staff=False,
            is_superuser=False
        )

    def test_avatar_label_is_correct(self):
        user = User.objects.get(username=self.username)
        avatar_label = user._meta.get_field('avatar').verbose_name
        self.assertEqual(avatar_label, 'avatar')

    def test_email_label(self):
        user = User.objects.get(username=self.username)
        field = user._meta.get_field('email')
        self.assertEqual(field.verbose_name, 'email address')
        self.assertTrue(field.blank)

    def test_city_max_length(self):
        user = User.objects.get(username=self.username)
        meta = user._meta.get_field('city')
        self.assertEqual(meta.max_length, 50)
        self.assertTrue(meta.null)
        self.assertTrue(meta.blank)

    def test_first_name_label(self):
        user = User.objects.get(username=self.username)
        field_label = user._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_first_name_max_length(self):
        user = User.objects.get(username=self.username)
        field_max_length = user._meta.get_field('first_name').max_length
        self.assertEqual(field_max_length, 150)

    def test_last_name_max_length(self):
        user = User.objects.get(username=self.username)
        field_max_length = user._meta.get_field('last_name').max_length
        self.assertEqual(field_max_length, 150)

    def test_last_name_label(self):
        user = User.objects.get(username=self.username)
        field_label = user._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_date_of_birth_label(self):
        user = User.objects.get(username=self.username)
        field_label = user._meta.get_field('birthday')
        self.assertEqual(field_label.max_length, None)
        self.assertTrue(field_label.null)
        self.assertTrue(field_label.blank)

    def test_username_label(self):
        user = User.objects.get(username=self.username)
        field = user._meta.get_field('username')
        self.assertTrue(field.max_length, len(self.username))
        self.assertTrue(field.unique, True)

    def test_user_str(self):
        user = User.objects.get(username=self.username)
        expected_object_name = '%s' % user.username
        self.assertEqual(expected_object_name, user.username)

    def test_is_activated_staff_superuser_user_status(self):
        user = User.objects.get(username=self.username)

        self.assertTrue(user.is_activated)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)


class TestMessage(TestCase):
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

        Message.objects.create(
            sender=User.objects.get(username=cls.username),
            recipient=User.objects.get(username=cls.username),
            subject='123',
            body='123',
        )

    def setUp(self):
        self.user = User.objects.get(username=self.username)
        self.message = Message.objects.get(sender=self.user, recipient=self.user)

    def test_sender_recipient_label(self):
        sender = self.message._meta.get_field('sender')
        recipient = self.message._meta.get_field('recipient')

        self.assertEqual(sender.null, recipient.null, True)
        self.assertEqual(sender.blank, recipient.blank, True)

    def test_id_label(self):
        pk = self.message._meta.get_field('id')

        self.assertEqual(pk.unique, True)
        self.assertEqual(pk.primary_key, True)
        self.assertEqual(pk.editable, False)
