from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_posts")
    body = models.CharField(max_length=225)
    time = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="liked_posts")

    def __str__(self):
        return f"{self.id} {self.user} {self.body}"

    def serialize(self):
        return {
            "id": self.id,
            "username": self.user.username,
            "body": self.body,
            "timestamp": self.time.strftime("%b %#d %Y, %#I:%M %p"),
        }

class profile(models.Model):
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followed_accounts")
    followee = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return f"{self.follower} is following {self.followee}"
