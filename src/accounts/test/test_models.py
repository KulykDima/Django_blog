from accounts.models import User

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
            is_activated=True
        )

    def setUp(self):
        self.user = User.objects.get(username=self.username)

    def test_avatar_label_is_correct(self):
        avatar_label = self.user._meta.get_field('avatar').verbose_name
        self.assertEqual(avatar_label, 'avatar')

    def test_city_max_length(self):
        meta = self.user._meta.get_field('city')
        self.assertEqual(meta.max_length, 50)
        self.assertTrue(meta.null)
        self.assertTrue(meta.blank)

    def test_convert_user_to_str(self):
        self.assertEqual(str(self.user), self.username)

    def test_first_name_label(self):
        field_label = self.user._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_first_name_max_length(self):
        field_max_length = self.user._meta.get_field('first_name').max_length
        self.assertEqual(field_max_length, 150)

    def test_last_name_max_length(self):
        field_max_length = self.user._meta.get_field('last_name').max_length
        self.assertEqual(field_max_length, 150)

    def test_last_name_label(self):
        field_label = self.user._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_date_of_birth(self):
        field_label = self.user._meta.get_field('birthday').verbose_name
        self.assertEqual(field_label, 'birthday')

    def test_birthday_blank(self):
        field_label = self.user._meta.get_field('birthday').blank
        self.assertTrue(field_label, self.user.birthday)

    def test_username_max_length(self):
        field_max_length = self.user._meta.get_field('username').max_length
        self.assertTrue(field_max_length, len(self.username))

    def test_user_str(self):
        expected_object_name = '%s' % self.user.username
        self.assertEqual(expected_object_name, self.user.username)

    def test_is_activated_staff_superuser(self):
        self.assertTrue(self.user.is_activated)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
