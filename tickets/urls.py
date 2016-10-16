# coding=utf-8

from django.conf.urls import url
from tickets.views import CreateTicketView, GetTicketView, GetMyTicketsView

urlpatterns = [
    url(r'^/?$', CreateTicketView.as_view()),
    url(r'^(?P<ticket_id>.[0-9a-fA-F]+)/?$', GetTicketView.as_view()),
    url(r'/mine/?$', GetMyTicketsView.as_view())
]