from django.test import TestCase
from django.urls import reverse

from .models import Post, User


class UserTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.user3 = User.objects.create(username='user3')
        self.user4 = User.objects.create(username='user4')
        self.user5 = User.objects.create(username='user5')
        self.user6 = User.objects.create(username='user6')
        self.user1.follows.add(self.user2, self.user3, self.user4)
        self.user2.follows.add(self.user5)
        self.user3.follows.add(self.user5, self.user6)
        self.user4.follows.add(self.user1, self.user2)
        self.user5.follows.add(self.user1, self.user3)

    def test_get_suggested_followers(self):
        suggested_followers = self.user1.get_suggested_followers()
        self.assertEqual(len(suggested_followers), 2)
        self.assertEqual(suggested_followers[0], self.user5)
        self.assertEqual(suggested_followers[1], self.user6)
        self.assertNotIn(self.user1, suggested_followers)


class LikeUnlikePostViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(creator=self.user)

    def test_like_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.put(reverse('like_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user, self.post.likers.all())

    def test_unlike_post(self):
        self.client.login(username='testuser', password='testpassword')
        self.post.likers.add(self.user)
        response = self.client.put(reverse('unlike_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.user, self.post.likers.all())
