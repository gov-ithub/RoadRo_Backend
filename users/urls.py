# coding=utf-8

from django.conf.urls import url
from users.views import RegistrationView

urlpatterns = [
    url(r'register/?$', RegistrationView.as_view()),
]