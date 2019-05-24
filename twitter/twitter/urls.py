"""twitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from app.views import UserRegistration, TweetAllView, MessageListView, MessageCreateView, MessageDetailView, \
    TweetDetailView
from twitter.settings import DEBUG

urlpatterns = [
    path('admin/', admin.site.urls),

    path('register/', UserRegistration.as_view(), name="register"),
    path('login/', LoginView.as_view(template_name="users/login.html"), name='login'),
    path('logout/', LogoutView.as_view(template_name="users/logged_out.html"), name='logout'),

    path('', TweetAllView.as_view(), name="home"),
    path('tweet/<int:pk>', TweetDetailView.as_view(), name="tweet-detail"),
    path('messages/', MessageListView.as_view(), name="messages"),
    path('messages/<int:pk>', MessageDetailView.as_view(), name="message_detail"),
    path('messages/create/', MessageCreateView.as_view(), name="create_message"),
]


if DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),

                  ] + urlpatterns
