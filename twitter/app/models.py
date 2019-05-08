import re

from django.contrib.auth.models import User
from django.db import models


class Tweet(models.Model):
    content = models.CharField(max_length=140)
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Posted on {self.creation_date.strftime('%b %d %Y %H:%M:%S')}"


class Comment(models.Model):
    content = models.CharField(max_length=140)
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)

    def __str__(self):
        return f"Commented on {self.creation_date.strftime('%b %d %Y %H:%M:%S')}"


class Message(models.Model):
    content = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')
    send_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message sent on {self.send_date.strftime('%b %d %Y %H:%M:%S')}"

    @property
    def content_wrap(self):
        wrap = ""
        string = " ".join(self.content.split('\n'))
        if len(string) > 30:
            for i in range(0, len(string) - 1):
                wrap += string[i]
                if i + 1 >= 30 and string[i + 1] is " ":
                    return f"{wrap}..."
        return string
