from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.log_in, name='log_in'),
		url(r'^home/$', views.home, name='home'),
        url(r'^logout/', views.log_out, name='log_out'),
]
