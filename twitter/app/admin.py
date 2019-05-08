from django.contrib import admin

from app.models import Tweet, Message, Comment

admin.site.register(Tweet)
admin.site.register(Message)
admin.site.register(Comment)
