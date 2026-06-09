from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post, Like, Comment, SavedPost


class PostModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_create_post(self):
        post = Post.objects.create(user=self.user, caption="Test caption")
        self.assertEqual(post.user, self.user)
        self.assertEqual(str(post), "testuser's Post (1)")

    def test_like_post(self):
        post = Post.objects.create(user=self.user)
        like = Like.objects.create(user=self.user, post=post)
        self.assertEqual(post.likes.count(), 1)
        self.assertEqual(str(like), "testuser likes Post 1")

    def test_comment_post(self):
        post = Post.objects.create(user=self.user)
        comment = Comment.objects.create(user=self.user, post=post, text="Nice!")
        self.assertEqual(post.comments.count(), 1)
        self.assertEqual(str(comment), "testuser's comment on Post 1")

    def test_saved_post(self):
        post = Post.objects.create(user=self.user)
        saved = SavedPost.objects.create(user=self.user, post=post)
        self.assertEqual(str(saved), "testuser saved Post 1")


class PostViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")

    def test_create_post_view(self):
        response = self.client.get(reverse("create-post"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/create_post.html")

    def test_feed_view(self):
        response = self.client.get(reverse("feed"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/feed.html")

    def test_post_detail_view(self):
        post = Post.objects.create(user=self.user, caption="Test")
        response = self.client.get(reverse("post-detail", args=[post.pk]))
        self.assertEqual(response.status_code, 200)
