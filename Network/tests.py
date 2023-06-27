import os

from django.test import TestCase
from django.urls import reverse

from .models import Post
from .models import User


# Suggestions Test:
# user1 --> user2,user3,user4
# user2 --> user5
# user3 --> user5,user6
# user4 --> user1,user2
# user5 --> user1, user3


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


class SearchViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.user.profile_pic = os.path.join("..", "static", "images", "no_pic.png")
        self.user.cover = os.path.join("..", "static", "images", "no_cover.jpeg")
        self.user.save()

    def test_search_with_query(self):
        Post.objects.create(creator=self.user, content_text='Hello world')
        Post.objects.create(creator=self.user, content_text='Test post')
        response = self.client.get(reverse('search'), {'query': 'hello'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')
        self.assertContains(response, 'Hello world')
        self.assertNotContains(response, 'Test post')

    def test_search_without_query(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')
        self.assertNotContains(response, 'Hello world')
        self.assertNotContains(response, 'Test post')
