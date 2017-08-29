from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    #######################
    # investigation types #
    #######################

    # list
    url(r'^investigation-types/$', 
        views.InvestigationTypeListView.as_view(), 
        name='investigation_type_list'),

    # create
    url(r'^investigation-type/create/$', 
        views.InvestigationTypeCreateView.as_view(), 
        name='investigation_type_create'),

    # detail
    url(r'^investigation-type/(?P<pk>\d+)$', 
        views.InvestigationTypeDetailView.as_view(), 
        name='investigation_type_detail'),

    # update
    url(r'^investigation-type/(?P<pk>\d+)/update/$', 
        views.InvestigationTypeUpdateView.as_view(), 
        name='investigation_type_update'),

    # delete
    url(r'^investigation-type/(?P<pk>\d+)/delete/$', 
        views.InvestigationTypeDeleteView.as_view(), 
        name='investigation_type_delete'),

    ###########
    # project #
    ###########

    # list
    url(r'^projects/$', 
        views.ProjectListView.as_view(), 
        name='project_list'),

    # create
    url(r'^project/create/$', 
        views.ProjectCreateView.as_view(), 
        name='project_create'),
    
    # detail
    url(r'^project/(?P<pk>\d+)$', 
        views.ProjectDetailView.as_view(), 
        name='project_detail'),

    # update
    url(r'^project/(?P<pk>\d+)/update/$', 
        views.ProjectUpdateView.as_view(), 
        name='project_update'),

    # delete
    url(r'^project/(?P<pk>\d+)/delete/$', 
        views.ProjectDeleteView.as_view(), 
        name='project_delete'),

    ################
    # element type #
    ################

    # list
    url(r'^element-types/$', 
        views.ElementTypeListView.as_view(), 
        name='element_type_list'),

    # create
    url(r'^element-type/create/$', 
        views.ElementTypeCreateView.as_view(), 
        name='element_type_create'),

    # detail
    url(r'^element-type/(?P<pk>\d+)$', 
        views.ElementTypeDetailView.as_view(), 
        name='element_type_detail'),

    # update
    url(r'^element-type/(?P<pk>\d+)/update/$', 
        views.ElementTypeUpdateView.as_view(), 
        name='element_type_update'),
    # delete
    url(r'^element-type/(?P<pk>\d+)/delete/$', 
        views.ElementTypeDeleteView.as_view(), 
        name='element_type_delete'),

    ############################
    # element field descriptor #
    ############################

    # list
    url(r'^element-field-descriptors/$', 
        views.ElementFieldDescriptorListView.as_view(), 
        name='element_field_descriptor_list'),
    
    # create
    url(r'^element-field-descriptor/create/$', 
        views.ElementFieldDescriptorCreateView.as_view(), 
        name='element_field_descriptor_create'),
    
    # detail
    url(r'^element-field-descriptor/(?P<pk>\d+)$', 
        views.ElementFieldDescriptorDetailView.as_view(), 
        name='element_field_descriptor_detail'),
    
    # update
    url(r'^element-field-descriptor/(?P<pk>\d+)/update/$', 
        views.ElementFieldDescriptorUpdateView.as_view(), 
        name='element_field_descriptor_update'),
    
    # delete
    url(r'^element-field-descriptor/(?P<pk>\d+)/delete/$', 
        views.ElementFieldDescriptorDeleteView.as_view(), 
        name='element_field_descriptor_delete'),

    ###########
    # element #
    ###########

    # list
    url(r'^elements/$', 
        views.ElementListView.as_view(), 
        name='element_list'),
    
    # create
    url(r'^element/create/$', 
        views.ElementCreateView.as_view(), 
        name='element_create'),
    
    # detail
    url(r'^element/(?P<pk>\d+)$', 
        views.ElementDetailView.as_view(), 
        name='element_detail'),
    
    # update
    url(r'^element/(?P<pk>\d+)/update/$', 
        views.ElementUpdateView.as_view(), 
        name='element_update'),
    
    # delete
    url(r'^element/(?P<pk>\d+)/delete/$', 
        views.ElementDeleteView.as_view(), 
        name='element_delete'),

    ############################
    # element char field value #
    ############################

    # list
    url(r'^element-char-field-values/$', 
        views.ElementCharFieldValueListView.as_view(), 
        name='element_char_field_value_list'),
    
    # create
    url(r'^element-char-field-value/create/$', 
        views.ElementCharFieldValueCreateView.as_view(), 
        name='element_char_field_value_create'),
    
    # detail
    url(r'^element-char-field-value/(?P<pk>\d+)$', 
        views.ElementCharFieldValueDetailView.as_view(), 
        name='element_char_field_value_detail'),
    
    # update
    url(r'^element-char-field-value/(?P<pk>\d+)/update/$', 
        views.ElementCharFieldValueUpdateView.as_view(), 
        name='element_char_field_value_update'),
    
    # delete
    url(r'^element-char-field-value/(?P<pk>\d+)/delete/$', 
        views.ElementCharFieldValueDeleteView.as_view(), 
        name='element_char_field_value_delete'),

    ############################
    # element text field value #
    ############################

    # list
    url(r'^element-text-field-values/$', 
        views.ElementTextFieldValueListView.as_view(), 
        name='element_text_field_value_list'),
    
    # create
    url(r'^element-text-field-value/create/$', 
        views.ElementTextFieldValueCreateView.as_view(), 
        name='element_text_field_value_create'),
    
    # detail
    url(r'^element-text-field-value/(?P<pk>\d+)$', 
        views.ElementTextFieldValueDetailView.as_view(), 
        name='element_text_field_value_detail'),
    
    # update
    url(r'^element-text-field-value/(?P<pk>\d+)/update/$', 
        views.ElementTextFieldValueUpdateView.as_view(), 
        name='element_text_field_value_update'),
    
    # delete
    url(r'^element-text-field-value/(?P<pk>\d+)/delete/$', 
        views.ElementTextFieldValueDeleteView.as_view(), 
        name='element_text_field_value_delete'),

    ############################
    # element date field value #
    ############################

    # list
    url(r'^element-date-field-values/$', 
        views.ElementDateFieldValueListView.as_view(), 
        name='element_date_field_value_list'),
    
    # create
    url(r'^element-date-field-value/create/$', 
        views.ElementDateFieldValueCreateView.as_view(), 
        name='element_date_field_value_create'),
    
    # detail
    url(r'^element-date-field-value/(?P<pk>\d+)$', 
        views.ElementDateFieldValueDetailView.as_view(), 
        name='element_date_field_value_detail'),
    
    # update
    url(r'^element-date-field-value/(?P<pk>\d+)/update/$', 
        views.ElementDateFieldValueUpdateView.as_view(), 
        name='element_date_field_value_update'),
    
    # delete
    url(r'^element-date-field-value/(?P<pk>\d+)/delete/$', 
        views.ElementDateFieldValueDeleteView.as_view(), 
        name='element_date_field_value_delete'),

    ############################
    # element url field value #
    ############################

    # list
    url(r'^element-url-field-values/$', 
        views.ElementUrlFieldValueListView.as_view(), 
        name='element_url_field_value_list'),
    
    # create
    url(r'^element-url-field-value/create/$', 
        views.ElementUrlFieldValueCreateView.as_view(), 
        name='element_url_field_value_create'),
    
    # detail
    url(r'^element-url-field-value/(?P<pk>\d+)$', 
        views.ElementUrlFieldValueDetailView.as_view(), 
        name='element_url_field_value_detail'),
    
    # update
    url(r'^element-url-field-value/(?P<pk>\d+)/update/$', 
        views.ElementUrlFieldValueUpdateView.as_view(), 
        name='element_url_field_value_update'),
    
    # delete
    url(r'^element-url-field-value/(?P<pk>\d+)/delete/$', 
        views.ElementUrlFieldValueDeleteView.as_view(), 
        name='element_url_field_value_delete'),
]
