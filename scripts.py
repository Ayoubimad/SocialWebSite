import random

from Network.models import *


def script():
    print("Starting script: Random following and Random post interact")
    users = User.objects.all()
    posts = Post.objects.all()
    Comment.objects.all().delete()
    for post in posts:
        post.savers.clear()
        post.likers.clear()
        post.comment_count = 0
        post.save()

    for user in users:
        user.follows.clear()
        num_to_follow = random.randint(1, int((len(users) - 1) / 2))
        users_to_follow = random.sample(list(users.exclude(id=user.id)), num_to_follow)
        num_to_interact = random.randint(1, len(posts) - 1)
        posts_to_interact = random.sample(list(posts), num_to_interact)
        for follow_user in users_to_follow:
            user.follows.add(follow_user)
        for post in posts_to_interact:
            if random.choice([True, False]):
                post.likers.add(user)
            if random.choice([True, False]):
                post.savers.add(user)
            if random.choice([True, False]):
                comment_content = "This is a random comment."
                comment = Comment(post=post, commenter=user, comment_content=comment_content)
                comment.save()
                post.comment_count += 1
                post.save()
