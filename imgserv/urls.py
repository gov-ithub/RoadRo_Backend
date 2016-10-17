# coding=utf-8

from django.conf.urls import url
from imgserv.views import ImgServeView

urlpatterns = [
    url(r'^(?P<img_id>[0-9a-zA-Z\-\_\/=]{40,100})/?$', ImgServeView.as_view())
]
