from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^backupdb/$', views.backupdb_view, name='backupdb'),
]
