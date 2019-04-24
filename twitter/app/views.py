from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from app.forms import UserRegistrationForm
from app.models import Tweet


class UserRegistration(SuccessMessageMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_message = "User %(username)s has been registered"
    success_url = reverse_lazy('login')


class TweetView(CreateView):
    model = Tweet
    fields = ['content']
    success_url = reverse_lazy('home')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data["object_list"] = Tweet.objects.filter(user=get_object_or_404(User, pk=self.request.user.id))\
            .order_by("-creation_date")
        return context_data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = get_object_or_404(User, pk=self.request.user.id)
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    # def post(self, request, *args, **kwargs):
    #