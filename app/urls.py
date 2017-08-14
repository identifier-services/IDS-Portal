from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^projects/$', views.ProjectListView.as_view(), name='projects'),
    url(r'^project/(?P<pk>\d+)$', views.ProjectDetailView.as_view(), name='project-detail'),

    url(r'^investigation-types/$', views.InvestigationTypeListView.as_view(), name='investigation-types'),
    url(r'^investigation-type/(?P<pk>\d+)$', views.InvestigationTypeDetailView.as_view(), name='investigation-type-detail'),

    url(r'^entity-types/$', views.EntityTypeListView.as_view(), name='entity-types'),
    url(r'^entity-type/(?P<pk>\d+)$', views.EntityTypeDetailView.as_view(), name='entity-type-detail'),
]
