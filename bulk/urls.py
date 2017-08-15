from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload/$', views.index, name='upload'),
    url(r'^download/$', views.index, name='download'),
]
