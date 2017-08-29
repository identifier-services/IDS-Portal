# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .models import (InvestigationType, Project, ElementType, 
    ElementFieldDescriptor, Element, ElementCharFieldValue,
    ElementTextFieldValue, ElementDateFieldValue, ElementUrlFieldValue)


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
        # TODO: do this better (no replace)
        context['type_name'] = verbose_name.replace(' ', '_')

        return context


class BaseGenericCreateView(generic.CreateView):
    template_name = 'app/generic_form.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(BaseGenericCreateView, self).get_context_data(**kwargs)
        verbose_name = self.model._meta.verbose_name
        context['page_name'] = 'Create %s' % verbose_name.title() 
        context['type_name'] = verbose_name
        return context

    def get_initial(self):
        parent_qs = self.request.GET.get('parent')
        initial = {}

        if parent_qs:
            parent_types = self.model.get_parent_types()

            #TODO: multiple parents

            if parent_types:
                try:
                    parts = iter(parent_qs.split(':'))
                    parent_name = next(parts)
                    parent_id = next(parts) 
                    parent_class = None

                    for parent_type in parent_types:
                        if parent_type['field_name'] == parent_name:
                            parent_class = parent_type['class']
                            break

                    initial = {
                        parent_name: parent_class.objects.get(pk=parent_id)
                    }
                except Exception as e:
                    # logger.debug(e)
                    print e

        return initial


class BaseGenericUpdateView(generic.UpdateView):
    template_name = 'app/generic_form.html'
    context_object_name = 'object'
    fields = '__all__' 


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


class InvestigationTypeCreateView(BaseGenericCreateView):
    model = InvestigationType


class InvestigationTypeDetailView(BaseGenericDetailView):
    model = InvestigationType


class InvestigationTypeUpdateView(BaseGenericUpdateView):
    model = InvestigationType
    fields = '__all__'


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


class ElementFieldDescriptorDetailView(BaseGenericDetailView):
    model = ElementFieldDescriptor


class ElementFieldDescriptorUpdateView(BaseGenericUpdateView):
    model = ElementFieldDescriptor


class ElementFieldDescriptorDeleteView(BaseGenericDeleteView):
    model = ElementFieldDescriptor

###########
# Element #
###########

class ElementListView(BaseGenericListView):
    model = Element


class ElementCreateView(BaseGenericCreateView):
    model = Element


class ElementDetailView(BaseGenericDetailView):
    model = Element


class ElementUpdateView(BaseGenericUpdateView):
    model = Element


class ElementDeleteView(BaseGenericDeleteView):
    model = Element

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
# Element Url Field Value #
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
