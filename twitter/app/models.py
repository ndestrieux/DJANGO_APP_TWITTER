from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Tweet(models.Model):
    content = models.CharField(max_length=140)
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Post created on {self.creation_date} by {self.user}"
