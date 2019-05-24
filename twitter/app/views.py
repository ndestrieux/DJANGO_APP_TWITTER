from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView

from app.forms import UserRegistrationForm, TweetForm, MessageForm, CommentForm
from app.models import Tweet, Message, Comment


class UserRegistration(SuccessMessageMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_message = "User %(username)s has been registered"
    success_url = reverse_lazy('login')


class TweetAllView(LoginRequiredMixin, CreateView):
    model = Tweet
    form_class = TweetForm
    success_url = reverse_lazy('home')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data["tweets"] = Tweet.objects.filter(
            user=get_object_or_404(User, pk=self.request.user.id),
            blocked=False
        ).order_by("-creation_date")
        return context_data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = get_object_or_404(User, pk=self.request.user.id)
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class TweetDetailView(LoginRequiredMixin, DetailView):
    model = Tweet

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data["comments"] = Comment.objects.filter(
            tweet=get_object_or_404(Tweet, pk=self.kwargs.get("pk")),
            blocked=False
        ).order_by("creation_date")
        context_data["form"] = CommentForm()
        return context_data

    def post(self, request, pk):
        form = CommentForm(request.POST)
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.user = get_object_or_404(User, pk=self.request.user.id)
            self.object.tweet = get_object_or_404(Tweet, pk=pk)
            self.object = form.save()
        return HttpResponseRedirect(reverse('tweet-detail', args=(pk, )))


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    ordering = ['-send_date']
    queryset = Message.objects.filter(blocked=False)

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nb_of_msg_not_read'] = len(Message.objects.filter(recipient=self.request.user.id, is_read=False))
        return context


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message

    def get_object(self, queryset=None):
        msg = super(MessageDetailView, self).get_object(queryset)
        if self.request.user == msg.recipient and msg.is_read is False:
            msg.is_read = True
            msg.save()
        return msg


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('messages')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.sender = get_object_or_404(User, pk=self.request.user.id)
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())
