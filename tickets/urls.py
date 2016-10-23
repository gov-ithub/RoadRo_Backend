# coding=utf-8

from django.conf.urls import url
from tickets.views import CreateTicketView, GetTicketView, GetMyTicketsView, LikeTicketView

urlpatterns = [
    url(r'^/?$', CreateTicketView.as_view()),
    url(r'^(?P<ticket_id>[0-9a-zA-Z\-\_\/=]{40,100})/like/?$', LikeTicketView.as_view()),
    url(r'^(?P<ticket_id>[0-9a-zA-Z\-\_\/=]{40,100})/$', GetTicketView.as_view()),
    url(r'mine/?$', GetMyTicketsView.as_view()),
]