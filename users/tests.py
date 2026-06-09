from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile, Follow


class UserModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123", email="test@example.com"
        )

    def test_profile_created_on_user_creation(self):
        self.assertTrue(Profile.objects.filter(user=self.user).exists())

    def test_profile_str(self):
        self.assertEqual(str(self.user.profile), "testuser's Profile")


class FollowModelTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="pass123")
        self.user2 = User.objects.create_user(username="user2", password="pass123")

    def test_follow_creation(self):
        follow = Follow.objects.create(follower=self.user1, following=self.user2)
        self.assertEqual(str(follow), "user1 follows user2")

    def test_unique_follow(self):
        Follow.objects.create(follower=self.user1, following=self.user2)
        with self.assertRaises(Exception):
            Follow.objects.create(follower=self.user1, following=self.user2)


class AuthViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_register_view_get(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")

    def test_register_view_post(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "new@example.com",
                "password1": "StrongPass1!",
                "password2": "StrongPass1!",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_login_view(self):
        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "testpass123"}
        )
        self.assertEqual(response.status_code, 302)

    def test_login_view_invalid(self):
        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "wrongpass"}
        )
        self.assertEqual(response.status_code, 200)
