from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^projects/$', views.ProjectListView.as_view(), name='projects'),
    url(r'^project/(?P<pk>\d+)$', views.ProjectDetailView.as_view(), name='project-detail'),

    url(r'^investigation-types/$', views.InvestigationTypeListView.as_view(), name='investigation-types'),
    url(r'^investigation-type/(?P<pk>\d+)$', views.InvestigationTypeDetailView.as_view(), name='investigation-type-detail'),

    url(r'^element-types/$', views.ElementTypeListView.as_view(), name='element-types'),
    url(r'^element-type/(?P<pk>\d+)$', views.ElementTypeDetailView.as_view(), name='element-type-detail'),
]
