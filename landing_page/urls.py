from django.conf.urls import url
from django.contrib import admin
from items import views
from .views import about, contact, home


urlpatterns = [
    url(r'^$', home, name='home'),
    url('^about/$', about, name='about'),
    url('^contact/$', contact, name='contact')


]