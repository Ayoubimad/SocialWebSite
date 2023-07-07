from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Count
from django.utils import timezone


class User(AbstractUser):
    profile_pic = models.ImageField(upload_to='profile_pic/')
    bio = models.TextField(max_length=160, blank=True, null=True)
    cover = models.ImageField(upload_to='covers/', blank=True)
    follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True)

    def __str__(self):
        return self.username

    def serialize(self):
        return {
            'id': self.id,
            "username": self.username,
            "profile_pic": self.profile_pic.url,
            "first_name": self.first_name,
            "last_name": self.last_name
        }

    def get_suggested_followers(self):
        followed_users = self.follows.all()
        suggested_users = User.objects.exclude(id=self.id).exclude(id__in=followed_users).filter(
            followed_by__in=followed_users)
        suggested_users = suggested_users.annotate(num_my_followers=Count('followed_by__follows')).order_by(
            '-num_my_followers')[:4]
        return suggested_users


class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    date_created = models.DateTimeField(default=timezone.now)
    content_text = models.TextField(max_length=140, blank=True)
    content_image = models.ImageField(upload_to='posts/', blank=True)
    likers = models.ManyToManyField(User, blank=True, related_name='likes')
    savers = models.ManyToManyField(User, blank=True, related_name='saved')
    comment_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Post ID: {self.id} (creator: {self.creator})"


class Category(models.Model):
    name = models.CharField(max_length=255, default='')
    posts = models.ManyToManyField(Post, related_name='categories')

    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenters')
    comment_content = models.TextField(max_length=90)
    comment_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Post: {self.post} | Commenter: {self.commenter}"

    def serialize(self):
        return {
            "post_id": self.post.id,
            "id": self.id,
            "commenter": self.commenter.serialize(),
            "body": self.comment_content,
            "timestamp": self.comment_time.strftime("%d %b %Y, %I:%M %p")
        }


class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name='chats')
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Chat ID: {self.id}"


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message ID: {self.id} | Chat ID: {self.chat.id} | Sender: {self.sender.username}"

    def serialize(self):
        return {
            'id': self.id,
            'chat_id': self.chat.id,
            'sender': self.sender.serialize(),
            'content': self.content,
            'timestamp': self.timestamp.strftime("%d %b %Y, %I:%M %p")
        }
