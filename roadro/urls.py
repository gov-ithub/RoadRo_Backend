# coding=utf-8

from django.conf.urls import url, include

urlpatterns = [
    url(r'api/v0/users/', include('users.urls')),
    url(r'api/v0/tickets/', include('tickets.urls')),
    url(r'images/', include('imgserv.urls'))
]
