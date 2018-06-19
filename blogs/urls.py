from django.conf.urls import url
from django.contrib import admin
from items import views
from .views import blog_list, blog_detail, testing


urlpatterns = [
    url('^blog/$', blog_list, name='list'),
    url('^blog/(?P<id>\d+)/$', blog_detail, name='detail'),
    url('^blog/test/$', testing, name='testing'),
]