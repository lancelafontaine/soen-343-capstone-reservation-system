from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^status/$', views.status, name='status'),
        url(r'^login/$', views.log_in, name='log_in'),
        url(r'^logout/$', views.log_out, name='log_out'),
        url(r'^getSessionInfo/$', views.getSessionInfo, name='getSessionInfo'),
        url(r'^getReservations/$', views.getReservations, name='getReservations'),
        url(r'^getRooms/$', views.getRooms, name='getRooms'),
        url(r'^getReservedList/$', views.getReservedList, name='getReservedList'),
        url(r'^getWaitingList/$', views.getWaitingList, name='getWaitingList'),
        url(r'^makeReservation/$', views.makeReservation, name='makeReservation'),
        url(r'^cancelReservation/$', views.cancelReservation, name='cancelReservation'),
        url(r'^modifyReservation/$', views.modifyReservation, name='modifyReservation'),
]
      # url(r'^modifyReservation/$', views.modifyReservation, name='modifyReservation'),
      # url(r'^cancelReservation/$', views.cancelReservation, name='cancelReservation'),
      # url(r'^viewReservations/$', views.viewReservations, name='viewReservations'),

