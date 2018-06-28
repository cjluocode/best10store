from django.conf.urls import url
from .views import search_result, item_detail


urlpatterns = [
    url(r'^result/$', search_result, name='result'),
    url(r'^items/detail/(?P<id>\d+)/$', item_detail, name='detail'),
]