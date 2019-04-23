from django.test import TestCase
from django.contrib.auth import get_user_model

class UserManagersTest(TestCase):
    
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="test@email.com", password="strong123")
        self.assertEqual(user.email, "test@email.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        # username is None for the AbstractUser
        self.assertIsNone(user.username)

        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="123")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser('sup@email.com', 'strong123')
        self.assertEqual(admin_user.email, 'sup@email.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        # username is None for the AbstractUser
        self.assertIsNone(admin_user.username)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(email='sup@email.com', password='123', is_superuser=False)
            