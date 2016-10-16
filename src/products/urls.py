from django.conf.urls import include, url
from django.contrib import admin

from .views import (
    ProductCreateView,
    ProductListView,
    ProductDetailView,
    ProductUpdateView,
    )

urlpatterns = [
    url(r'^$', ProductListView.as_view(), name='list'),
    url(r'^add/$', ProductCreateView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', ProductDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/$', ProductDetailView.as_view(), name='detail_slug'),
    url(r'^(?P<pk>\d+)/edit/$', ProductUpdateView.as_view(), name='update'),
    url(r'^(?P<slug>[\w-]+)/edit/$', ProductUpdateView.as_view(), name='update_slug'),
]
