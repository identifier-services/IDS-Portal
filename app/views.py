# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core import paginator
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

import logging
import requests

from zipfile import ZipFile
import csv
import urllib
from zipfile import ZipFile

import logging

from .models import (InvestigationType, Project, ElementType,
    RelationshipDefinition, ElementFieldDescriptor, Element, Checksum, Dataset,
    ElementCharFieldValue, ElementTextFieldValue, ElementIntFieldValue,
    ElementFloatFieldValue, ElementDateFieldValue, ElementUrlFieldValue)

from .forms import ProjectForm

logger = logging.getLogger(__name__)

##############
# Base Views #
##############

class BaseGenericListView(generic.ListView):
    template_name = 'app/generic_list.html'
    context_object_name = 'object_list'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        # logger.debug('request user: %s' % self.request.user)
        # logger.debug('dir(request.user): %s' % dir(self.request.user))

        context = super(BaseGenericListView, self).get_context_data(**kwargs)
        verbose_name = self.model._meta.verbose_name
        context['verbose_name'] = verbose_name.title()
        context['type_name'] = verbose_name.replace(' ', '_')
        context['create_url'] = self.model.get_create_url()
        return context


class BaseGenericDetailView(generic.DetailView):
    template_name = 'app/generic_detail.html'
    context_object_name = 'object'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(BaseGenericDetailView, self).get_context_data(**kwargs)
        verbose_name = self.model._meta.verbose_name
        context['verbose_name'] = verbose_name.title()
        context['type_name'] = verbose_name.replace(' ', '_')

        if self.model == InvestigationType:
            return context

        if self.model == Project:
            project = context['object']
        else:
            project = context['object'].project

        inv_type = project.investigation_type
        elem_types = inv_type.elementtype_set.all()

        contents = {}

        for elem_type in elem_types:
            contents[elem_type.name] = {
                'link': '%s?project=%s&element=%s' % (
                    reverse_lazy('app:element_list'),
                    project.name,
                    elem_type.name
                ),
                'count': Element.objects.filter(
                    element_type=elem_type,
                    project=project
                ).count()
            }

        contents['dataset'] = {
                'link': '%s?project=%s' % (
                    reverse_lazy('app:dataset_list'),
                    project.name
                ),
                'count': Dataset.objects.filter(
                    project=project
                ).count()
            }

        context['contents'] = contents

        graph = {
            'height': '740',
            'width': '740',
            'nodes': [
                {
                    'x': '0',
                    'y': '0',
                    'element_count': '1',
                    'element_type_name': inv_type.name,
                    'url': reverse_lazy(
                        'app:investigation_type_detail',
                        kwargs={'pk': inv_type.id}
                    ),
                },
                {
                    'x': '200',
                    'y': '0',
                    'element_count': '1',
                    'element_type_name': project.name,
                    'url': reverse_lazy(
                        'app:project_detail',
                        kwargs={'pk': project.id}
                    ),
                },
                {
                    'x': '200',
                    'y': '200',
                    'element_count': contents['specimen']['count'],
                    'element_type_name': 'Specimen',
                    'url': contents['specimen']['link'],
                },
                {
                    'x': '400',
                    'y': '200',
                    'element_count': contents['chunk']['count'],
                    'element_type_name': 'Chunk',
                    'url': contents['chunk']['link'],
                },
                {
                    'x': '200',
                    'y': '400',
                    'element_count': contents['probe']['count'],
                    'element_type_name': 'Probe',
                    'url': contents['probe']['link'],
                },
                {
                    'x': '400',
                    'y': '400',
                    'element_count': contents['process']['count'],
                    'element_type_name': 'Process',
                    'url': contents['process']['link'],
                },
                {
                    'x': '400',
                    'y': '600',
                    'element_count': contents['image']['count'],
                    'element_type_name': 'Image',
                    'url': contents['image']['link'],
                },
                {
                    'x': '600',
                    'y': '600',
                    'element_count': contents['dataset']['count'],
                    'element_type_name': 'Dataset',
                    'url': contents['dataset']['link'],
                },
            ],
            'edges': [                                                          
                {
                    'x': '100',
                    'y': '50',
                    'direction': 'right',
                },
                {
                    'x': '300',
                    'y': '250',
                    'direction': 'right',
                },
                {
                    'x': '450',
                    'y': '300',
                    'direction': 'down',
                },
                {
                    'x': '300',
                    'y': '450',
                    'direction': 'right',
                },
                {
                    'x': '450',
                    'y': '500',
                    'direction': 'down',
                },
                {
                    'x': '500',
                    'y': '650',
                    'direction': 'right',
                },
            ]
        }

        context['graph'] = graph

        return context


class BaseGenericCreateView(generic.CreateView):
    template_name = 'app/generic_form.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(BaseGenericCreateView, self).get_context_data(**kwargs)
        verbose_name = self.model._meta.verbose_name
        context['verbose_name'] = verbose_name.title()
        context['type_name'] = verbose_name.replace(' ', '_')
        return context

    def get_initial(self):
        parent_qs = self.request.GET.get('parent')
        initial = {}

        if parent_qs:
            parent_types = self.model.get_parent_types()
            if not parent_types:
                return None

            for parent in parent_qs.split(','):
                try:
                    parent_name, parent_id = parent.split(':')
                    parent_class = filter(
                        lambda x,y=parent_name: x['field_name'] == parent_name,
                        parent_types).pop().get('class')

                    initial.update({
                        parent_name: parent_class.objects.get(pk=parent_id)
                    })
                except Exception as e:
                    logger.debug(e)

        return initial


class BaseGenericUpdateView(generic.UpdateView):
    template_name = 'app/generic_form.html'
    context_object_name = 'object'
    fields = '__all__'


class BaseGenericDeleteView(generic.DeleteView):
    template_name = 'app/generic_delete.html'
    context_object_name = 'object'

    # the success url is difficult to determine, it's going to get
    # complicated with anything other than project or investigation lists
    success_url = reverse_lazy('app:project_list')

    def get_context_data(self, **kwargs):
        context = super(BaseGenericDeleteView, self).get_context_data(**kwargs)
        verbose_name = self.model._meta.verbose_name
        context['type_name'] = verbose_name

        # set the success_url to the parent, if there is one.
        # this is hacky, but then the whole thing is
        context_object = context['object']
        parent_rels = context_object.get_parent_relations()
        if parent_rels:

            # just get the first parent
            parent_rel = next(iter(parent_rels))

            try:
                success_url = reverse_lazy('%s_detail' % parent_rel['field_name'])
            except Exception as e:
                logger.debug(e)

        return context

    def post(self, request, *args, **kwargs):
        if "Cancel" in request.POST:
            url = self.success_url
            if not url:
                url = reverse_lazy('app:project_list')
            return HttpResponseRedirect(url) 
        else:
            return super(BaseGenericDeleteView, self).post(
                request, *args, **kwargs)

#############
# Home Page #
#############

def index(request):
    """home page"""
    return render (request, 'app/index.html', context={})

######################
# Investigation Type #
######################

class InvestigationTypeListView(BaseGenericListView):
    model = InvestigationType


class InvestigationTypeCreateView(BaseGenericCreateView):
    model = InvestigationType


class InvestigationTypeDetailView(BaseGenericDetailView):
    model = InvestigationType


class InvestigationTypeUpdateView(BaseGenericUpdateView):
    model = InvestigationType
    fields = '__all__'


class InvestigationTypeDeleteView(BaseGenericDeleteView):
    model = InvestigationType

###########
# Project #
###########

class ProjectListView(BaseGenericListView):
    model = Project


class ProjectCreateView(BaseGenericCreateView):
    model = Project


class ProjectDetailView(BaseGenericDetailView):
    model = Project


class ProjectUpdateView(BaseGenericUpdateView):
    model = Project


class ProjectDeleteView(BaseGenericDeleteView):
    model = Project

################
# Element Type #
################

class ElementTypeListView(BaseGenericListView):
    model = ElementType


class ElementTypeCreateView(BaseGenericCreateView):
    model = ElementType


class ElementTypeDetailView(BaseGenericDetailView):
    model = ElementType


class ElementTypeUpdateView(BaseGenericUpdateView):
    model = ElementType


class ElementTypeDeleteView(BaseGenericDeleteView):
    model = ElementType


############################
# Element Field Descriptor #
############################

class ElementFieldDescriptorListView(BaseGenericListView):
    model = ElementFieldDescriptor


class ElementFieldDescriptorCreateView(BaseGenericCreateView):
    model = ElementFieldDescriptor
    fields = '__all__'


class ElementFieldDescriptorDetailView(generic.DetailView):
    model = ElementFieldDescriptor
    template_name = 'app/field_descriptor_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ElementFieldDescriptorDetailView, self)\
            .get_context_data(**kwargs)
        descriptor = context['object']

        try:
            context['value_type'] = descriptor.verbose_value_type
        except Exception as e:
            logger.debug(e)

        return context


class ElementFieldDescriptorUpdateView(BaseGenericUpdateView):
    model = ElementFieldDescriptor


class ElementFieldDescriptorDeleteView(BaseGenericDeleteView):
    model = ElementFieldDescriptor

###########################
# Relationship Definition #
###########################

class RelationshipDefinitionListView(BaseGenericListView):
    model = RelationshipDefinition


class RelationshipDefinitionCreateView(BaseGenericCreateView):
    model = RelationshipDefinition
    fields = '__all__'


class RelationshipDefinitionDetailView(generic.DetailView):
    model = RelationshipDefinition
    template_name = 'app/relationship_definition_detail.html'

    def get_context_data(self, **kwargs):
        context = super(RelationshipDefinitionDetailView, self)\
            .get_context_data(**kwargs)
        definition = context['object']

        try:
            context['rel_type'] = definition.verbose_relationship_type
        except Exception as e:
            logger.debug(e)

        try:
            context['card'] = definition.verbose_cardinality
        except Exception as e:
            logger.debug(e)

        return context


class RelationshipDefinitionUpdateView(BaseGenericUpdateView):
    model = RelationshipDefinition


class RelationshipDefinitionDeleteView(BaseGenericDeleteView):
    model = RelationshipDefinition

###########
# Element #
###########


def element_init_checksum(request, pk):
    try:
        element = Element.objects.get(id=pk)
        element.initiate_checksum()
    except Exception as e:
        logger.error(e)
        return HttpResponseRedirect(reverse_lazy('app:project_list'))

    return HttpResponseRedirect(reverse_lazy(
            'app:element_detail',kwargs={'pk': pk}))


class ElementListView(BaseGenericListView):
    model = Element

    def get_queryset(self):
        return_json = False
        heirarchical_filters = []
        kv_queries = []

        for k,v in self.request.GET.items():
            k = k.lower().replace('_','').replace('-','')

            # investigation type query
            if k in ['inv', 'investigation', 'invtype','investigationtype']:
                heirarchical_filters.append(
                    Q(project__investigation_type__name__iexact=v))
                    # Q(project__investigation_type__id=v))

            # project query
            elif k in ['proj','project']:
                heirarchical_filters.append(
                    Q(project__name__iexact=v))
                    # Q(project__id=v))

            # path query
            elif k == 'path':
                heirarchical_filters.append(
                    Q(path_id=v))

            # element type query
            elif k in ['elem','element','elemtype','elementtype']:
                heirarchical_filters.append(
                    Q(element_type__name__iexact=v))

            # return json?
            elif k == 'json':
                return_json = True

            # ignore paging
            elif k == 'page':
                continue

            # query by element field values
            else:
                kv_queries.append((k,v))
        
        if heirarchical_filters:
            query_set = Element.objects.filter(*heirarchical_filters)
        else:
            query_set = Element.objects.all()

        if kv_queries:
            field_values  =[]
            
            for k,v in kv_queries:
                field_values.extend(
                    [descr.value_type.objects.filter(
                        element__in=query_set, 
                        value__icontains=v
                    ) for descr in ElementFieldDescriptor.objects.filter(
                        label__iexact=k
                    )])

            filter_by_values = Q(id__in=[v.element.id for qs in field_values for v in qs])
            query_set = Element.objects.filter(filter_by_values)

        return query_set

class ElementCreateView(BaseGenericCreateView):
    model = Element


class ElementDetailView(BaseGenericDetailView):#generic.DetailView):
    model = Element
    template_name = 'app/element_detail.html'

    def get_context_data(self, **kwargs):

        context = super(ElementDetailView, self).get_context_data(**kwargs)

        verbose_name = self.model._meta.verbose_name
        context['verbose_name'] = verbose_name.title() 
        context['type_name'] = verbose_name.replace(' ', '_')

        context_object = context['object']
        descriptors = \
            context_object.element_type.elementfielddescriptor_set.filter(
                element_type__element=context_object
            )

        values = []
        for descriptor in descriptors:
            # get descriptor attributes
            label = descriptor.label
            help_text = descriptor.help_text
            
            # get the values
            value_type = descriptor.value_type

            # TODO: what if more than one field value? how to prevent?
            field_value = value_type.objects.filter(
                element = context_object,
                element_field_descriptor=descriptor
            ).first()

            if field_value:
                action_url = '%s/update' % field_value.get_absolute_url()
                action = 'Edit'
            else:
                descriptor_field_name = \
                    descriptor._meta.verbose_name.replace(' ', '_')

                parents_qs = '?parent=%s:%s,%s:%s' % (
                    descriptor_field_name, descriptor.id,
                    context['type_name'], context_object.id
                )
                action_url = '%s%s' % (value_type.get_create_url(), parents_qs)
                action = 'Set'

            type_id = descriptor.id

            values.append({
                'label': label,
                'help_text': help_text,
                'field_value': field_value,
                'action_url': action_url,
                'action': action,
            })
        context['values'] = values

        ordered_sums = Checksum.objects.filter(
            data=context_object.id).order_by('initiated')

        sums = []

        standard = None
        for checksum in ordered_sums:
            if checksum.status == Checksum.CMP and checksum.value:
                standard = {
                    'value': checksum.value, 
                }
                break

        ordered_sums.reverse()

        if standard:
            for checksum in ordered_sums:
                status = 'in progress'
                if checksum.value == standard['value']:
                    status = 'good'
                elif checksum.error_message:
                    status = 'failed'
                elif checksum.status == Checksum.CMP:
                    status = 'conflict'
                    
                sums.append({
                    'status':status,
                    'link':checksum.get_absolute_url(),
                    'message':checksum.error_message,
                    'date':checksum.initiated
                })
        else:
            for checksum in ordered_sums:
                status = 'in progress'
                if checksum.error_message:
                    status = 'failed'
                elif checksum.status == Checksum.CMP:
                    status = 'conflict'

                sums.append({
                    'status':status,
                    'link':checksum.get_absolute_url(),
                    'message':checksum.error_message,
                    'date':checksum.initiated
                })

        context['checksums'] = sums

        return context


class ElementUpdateView(BaseGenericUpdateView):
    model = Element


class ElementDeleteView(BaseGenericDeleteView):
    model = Element

###########
# Dataset #
###########

def request_doi(request, pk):
    try:
        dataset = Dataset.objects.get(id=pk)
        dataset.request_doi()

        headers = {"Content-Type": "application/json"}
        r = requests.post('https://zenodo.org/api/deposit/depositions',
                params={'access_token': settings.ZENODO_TOKEN}, json={},
                headers=headers)
        dataset.doi = r.json()['metadata']['prereserve_doi']['doi']
        dataset.save()

    except Exception as e:
        logger.error(e)
        return HttpResponseRedirect(reverse_lazy('app:project_list'))

    return HttpResponseRedirect(reverse_lazy(
            'app:dataset_detail',kwargs={'pk': pk}))


class DatasetListView(BaseGenericListView):
    model = Dataset


class DatasetCreateView(BaseGenericCreateView):
    model = Dataset


class DatasetDetailView(BaseGenericDetailView):
    model = Dataset
    template_name = 'app/dataset_detail.html'

    def get_context_data_(self, **kwargs):
        context = super(DatasetDetailView, self).get_context_data(**kwargs)
        verbose_name = self.model._meta.verbose_name
        context['verbose_name'] = verbose_name.title() 
        context['type_name'] = verbose_name.replace(' ', '_')

        # context_object = context['object']

        graph = {
            'height': '740',
            'width': '740',
            'nodes': [
                {
                    'x': '0',
                    'y': '0',
                    'element_count': '1',
                    'element_type_name': 'Lungmap',
                    'url': reverse_lazy('app:investigation_type_list'),
                },
                {
                    'x': '200',
                    'y': '0',
                    'element_count': '1',
                    'element_type_name': 'Project',
                    'url': reverse_lazy('app:project_list'),
                },
                {
                    'x': '200',
                    'y': '200',
                    'element_count': '10',
                    'element_type_name': 'Specimen',
                    'url': reverse_lazy('app:element_list'),
                },
                {
                    'x': '400',
                    'y': '200',
                    'element_count': '30',
                    'element_type_name': 'Chunk',
                    'url': reverse_lazy('app:element_list'),
                },
                {
                    'x': '200',
                    'y': '400',
                    'element_count': '1',
                    'element_type_name': 'Probe',
                    'url': reverse_lazy('app:element_list'),
                },
                {
                    'x': '400',
                    'y': '400',
                    'element_count': '30',
                    'element_type_name': 'Process',
                    'url': reverse_lazy('app:element_list'),
                },
                {
                    'x': '400',
                    'y': '600',
                    'element_count': '30',
                    'element_type_name': 'Image',
                    'url': reverse_lazy('app:element_list'),
                },
                {
                    'x': '600',
                    'y': '600',
                    'element_count': '1',
                    'element_type_name': 'Dataset',
                    'url': reverse_lazy('app:dataset_list'),
                },
            ],
            'edges': [                                                          
                {
                    'x': '100',
                    'y': '50',
                    'direction': 'right',
                },
                {
                    'x': '300',
                    'y': '250',
                    'direction': 'right',
                },
                {
                    'x': '450',
                    'y': '300',
                    'direction': 'down',
                },
                {
                    'x': '300',
                    'y': '450',
                    'direction': 'right',
                },
                {
                    'x': '450',
                    'y': '500',
                    'direction': 'down',
                },
                {
                    'x': '500',
                    'y': '650',
                    'direction': 'right',
                },
            ]
        }

        context['graph'] = graph

        return context


class DatasetUpdateView(BaseGenericUpdateView):
    model = Dataset


class DatasetDeleteView(BaseGenericDeleteView):
    model = Dataset

############################
# Element Char Field Value #
############################

class ElementCharFieldValueListView(BaseGenericListView):
    model = ElementCharFieldValue


class ElementCharFieldValueCreateView(BaseGenericCreateView):
    model = ElementCharFieldValue


class ElementCharFieldValueDetailView(BaseGenericDetailView):
    model = ElementCharFieldValue


class ElementCharFieldValueUpdateView(BaseGenericUpdateView):
    model = ElementCharFieldValue


class ElementCharFieldValueDeleteView(BaseGenericDeleteView):
    model = ElementCharFieldValue


############################
# Element Text Field Value #
############################

class ElementTextFieldValueListView(BaseGenericListView):
    model = ElementTextFieldValue


class ElementTextFieldValueCreateView(BaseGenericCreateView):
    model = ElementTextFieldValue


class ElementTextFieldValueDetailView(BaseGenericDetailView):
    model = ElementTextFieldValue


class ElementTextFieldValueUpdateView(BaseGenericUpdateView):
    model = ElementTextFieldValue


class ElementTextFieldValueDeleteView(BaseGenericDeleteView):
    model = ElementTextFieldValue

############################
# Element Int Field Value #
############################

class ElementIntFieldValueListView(BaseGenericListView):
    model = ElementIntFieldValue


class ElementIntFieldValueCreateView(BaseGenericCreateView):
    model = ElementIntFieldValue


class ElementIntFieldValueDetailView(BaseGenericDetailView):
    model = ElementIntFieldValue


class ElementIntFieldValueUpdateView(BaseGenericUpdateView):
    model = ElementIntFieldValue


class ElementIntFieldValueDeleteView(BaseGenericDeleteView):
    model = ElementIntFieldValue

#############################
# Element Float Field Value #
#############################

class ElementFloatFieldValueListView(BaseGenericListView):
    model = ElementFloatFieldValue


class ElementFloatFieldValueCreateView(BaseGenericCreateView):
    model = ElementFloatFieldValue


class ElementFloatFieldValueDetailView(BaseGenericDetailView):
    model = ElementFloatFieldValue


class ElementFloatFieldValueUpdateView(BaseGenericUpdateView):
    model = ElementFloatFieldValue


class ElementFloatFieldValueDeleteView(BaseGenericDeleteView):
    model = ElementFloatFieldValue

############################
# Element Date Field Value #
############################

class ElementDateFieldValueListView(BaseGenericListView):
    model = ElementDateFieldValue


class ElementDateFieldValueCreateView(BaseGenericCreateView):
    model = ElementDateFieldValue


class ElementDateFieldValueDetailView(BaseGenericDetailView):
    model = ElementDateFieldValue


class ElementDateFieldValueUpdateView(BaseGenericUpdateView):
    model = ElementDateFieldValue


class ElementDateFieldValueDeleteView(BaseGenericDeleteView):
    model = ElementDateFieldValue

############################
# Element Url Field Value  #
############################

class ElementUrlFieldValueListView(BaseGenericListView):
    model = ElementUrlFieldValue


class ElementUrlFieldValueCreateView(BaseGenericCreateView):
    model = ElementUrlFieldValue


class ElementUrlFieldValueDetailView(BaseGenericDetailView):
    model = ElementUrlFieldValue


class ElementUrlFieldValueUpdateView(BaseGenericUpdateView):
    model = ElementUrlFieldValue


class ElementUrlFieldValueDeleteView(BaseGenericDeleteView):
    model = ElementUrlFieldValue

############
# Checksum #
############

class ChecksumListView(BaseGenericListView):
    model = Checksum


class ChecksumCreateView(BaseGenericCreateView):
    model = Checksum


class ChecksumDetailView(BaseGenericDetailView):
    model = Checksum


#class ChecksumUpdateView(BaseGenericUpdateView):
#    model = Checksum

@csrf_exempt
def checksum_update(request, pk, *args, **kwargs):
    data_id = None
    try:
        checksum = Checksum.objects.get(id=pk)
        value = request.POST.get('checksum', None)
        err_msg = request.POST.get('error', None)

        if value:
            checksum.value = value
            checksum.status = 'CMP'
        if err_msg:
            checksum.error_message = err_msg
            checksum.status = 'ERR'

        if value or err_msg:
            checksum.save()
    except Exception as e:
        logger.error(e)
        return HttpResponse('Error: %s' % e)

    return HttpResponse('OK')


class ChecksumDeleteView(BaseGenericDeleteView):
    model = Checksum

