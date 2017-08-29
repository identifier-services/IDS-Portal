# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .models import InvestigationType, Project, ElementType, ElementFieldDescriptor, Element, ElementCharFieldValue


##############
# Base Views #
##############

class BaseGenericListView(generic.ListView):
    template_name = 'app/generic_list.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super(BaseGenericListView, self).get_context_data(**kwargs)
        verbose_name = self.model._meta.verbose_name
        context['page_name'] = '%s List' % verbose_name.title() 
        context['type_name'] = verbose_name
        context['create_url'] = self.model.get_create_url()
        return context


class BaseGenericDetailView(generic.DetailView):
    template_name = 'app/generic_detail.html'
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super(BaseGenericDetailView, self).get_context_data(**kwargs)
        verbose_name = self.model._meta.verbose_name
        context['page_name'] = '%s Detail' % verbose_name.title() 
        context['type_name'] = verbose_name
        return context


class BaseGenericCreateView(generic.CreateView):
    fields = '__all__'
    template_name = 'app/generic_form.html'

    def get_context_data(self, **kwargs):
        context = super(BaseGenericCreateView, self).get_context_data(**kwargs)
        verbose_name = self.model._meta.verbose_name
        context['page_name'] = 'Create %s' % verbose_name.title() 
        context['type_name'] = verbose_name
        return context

    def get_initial(self):
        parent_id = self.request.GET.get('parent')
        initial = {}

        if parent_id:
            parent_types = self.model.get_parent_types()

            #TODO: multiple parents

            if parent_types:
                try:
                    # just grab the first parent until we fix this
                    parent_type = next(iter(parent_types))
                    field_name = parent_type['field_name']
                    parent_class = parent_type['class']

                    initial = {
                        field_name: parent_class.objects.get(pk=parent_id)
                    }
                except Exception as e:
                    # logger.debug(e)
                    print e

        return initial


class BaseGenericDeleteView(generic.DeleteView):
    template_name = 'app/generic_delete.html'
    context_object_name = 'object'
    success_url = reverse_lazy('app:index')

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
                success_url = reverse('%s_detail' % parent_rel['field_name'])
            except Exception as e:
                # logger.debug(e)
                print e

        return context

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


class InvestigationTypeCreateView(generic.CreateView):
    model = InvestigationType
    fields = '__all__'


class InvestigationTypeDetailView(BaseGenericDetailView):
    model = InvestigationType


class InvestigationTypeUpdateView(generic.UpdateView):
    model = InvestigationType


class InvestigationTypeDeleteView(BaseGenericDeleteView):
    model = InvestigationType
    # success_url = reverse('app:index')

###########
# Project #
###########

class ProjectListView(BaseGenericListView):
    model = Project


class ProjectCreateView(BaseGenericCreateView):
    model = Project


class ProjectDetailView(BaseGenericDetailView):
    model = Project


class ProjectUpdateView(generic.UpdateView):
    model = Project


class ProjectDeleteView(BaseGenericDeleteView):
    model = Project

################
# Element Type #
################

class ElementTypeListView(BaseGenericListView):
    model = ElementType


class ElementTypeCreateView(generic.CreateView):
    model = ElementType
    fields = '__all__'

    def get_initial(self):
        
        print 'parent type: %s' % self.model.get_parent_type()

        parent_id = self.request.GET.get('parent')
        initial = {}

        if parent_id:
            initial = {
                'investigation_type': InvestigationType.objects.get(pk=parent_id)
            }

        return initial


class ElementTypeDetailView(BaseGenericDetailView):
    model = ElementType


class ElementTypeUpdateView(generic.UpdateView):
    model = ElementType


class ElementTypeDeleteView(BaseGenericDeleteView):
    model = ElementType



############################
# Element Field Descriptor #
############################

class ElementFieldDescriptorListView(BaseGenericListView):
    model = ElementFieldDescriptor


class ElementFieldDescriptorCreateView(generic.CreateView):
    model = ElementFieldDescriptor
    fields = '__all__'


class ElementFieldDescriptorDetailView(generic.DetailView):
    model = ElementFieldDescriptor


class ElementFieldDescriptorUpdateView(generic.UpdateView):
    model = ElementFieldDescriptor


class ElementFieldDescriptorDeleteView(generic.DeleteView):
    model = ElementFieldDescriptor

###########
# Element #
###########

class ElementListView(BaseGenericListView):
    model = Element


class ElementCreateView(generic.CreateView):
    model = Element
    fields = '__all__'


class ElementDetailView(generic.DetailView):
    model = Element


class ElementUpdateView(generic.UpdateView):
    model = Element


class ElementDeleteView(generic.DeleteView):
    model = Element

############################
# Element Char Field Value #
############################

class ElementCharFieldValueListView(BaseGenericListView):
    model = ElementCharFieldValue


class ElementCharFieldValueCreateView(generic.CreateView):
    model = ElementCharFieldValue
    fields = '__all__'


class ElementCharFieldValueDetailView(generic.DetailView):
    model = ElementCharFieldValue


class ElementCharFieldValueUpdateView(generic.UpdateView):
    model = ElementCharFieldValue


class ElementCharFieldValueDeleteView(generic.DeleteView):
    model = ElementCharFieldValue

