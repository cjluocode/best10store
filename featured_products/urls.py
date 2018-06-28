from django.conf.urls import url
from django.contrib import admin
from items import views
from .views import product_detail


urlpatterns = [
    # url(r'^products/save$', save_product, name='save'),
    url(r'^products/detail/(?P<id>\d+)/$',product_detail, name='product-detail'),
]