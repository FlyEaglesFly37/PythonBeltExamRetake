from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.createUser),
    url(r'^login$', views.login),
    url(r'^travels$', views.travels),
    url(r'^addtrip$', views.addtrip),
    url(r'^posttrip$', views.postTrip),
    url(r'^view/(?P<trip_id>\d+)$', views.view),
    url(r'^logout$', views.logout),
    url(r'^delete/(?P<trip_id>\d+)$', views.delete),
    url(r'^join$', views.join),
    url(r'^cancel/(?P<trip_id>\d+)$', views.cancel)
]