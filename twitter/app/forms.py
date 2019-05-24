from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder, Div
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from app.models import Tweet, Message, Comment


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class TweetForm(forms.ModelForm):

    class Meta:
        model = Tweet
        fields = ["content", ]
        labels = {
            "content": ""
        }
        widgets = {
            "content": forms.TextInput(
                attrs={"placeholder": "What's on your mind?"})
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["content", ]
        labels = {
            "content": ""
        }
        widgets = {
            "content": forms.TextInput(
                attrs={"placeholder": "Reply..."})
        }


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ['recipient', 'content', ]
        labels = {
            "recipient": "To:",
            "content": ""
        }
        widgets = {
            "content": forms.Textarea(
                attrs={"placeholder": "Message..."})
        }
