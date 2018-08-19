from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^backupdb/$', views.backupdb_view, name='backupdb'),
    url(r'^singlepost/<int:pk>/$', views.singlepost_view),
]
