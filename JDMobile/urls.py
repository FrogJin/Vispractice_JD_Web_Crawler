from django.conf.urls import *
from . import views

urlpatterns = [
	url(r'^search', views.search),
	url(r'^(?P<mobile_code>\d+)/$', views.detail, name="detail")
]
