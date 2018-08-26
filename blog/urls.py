from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^backupdb/$', views.backupdb_view, name='backupdb'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_view, name='post'),
    url(r'^jsonpost/(?P<pk>[0-9]+)/$', views.jsonpost_view, name='jsonpost'),
    url(r'^nextpost/(?P<pk>[0-9]+)/$', views.nextpost_view, name='nextpost'),
    url(r'^prevpost/(?P<pk>[0-9]+)/$', views.prevpost_view, name='prevpost'),
]
