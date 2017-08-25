# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import generic

from .models import InvestigationType, Project, ElementType, ElementFieldDescriptor, Element, ElementCharFieldValue


#############
# Home Page #
#############

def index(request):
    """home page"""
    return render (request, 'app/index.html', context={})

######################
# Investigation Type #
######################

class InvestigationTypeListView(generic.ListView):
    model = InvestigationType


class InvestigationTypeCreateView(generic.CreateView):
    model = InvestigationType
    fields = '__all__'


class InvestigationTypeDetailView(generic.DetailView):
    model = InvestigationType


class InvestigationTypeUpdateView(generic.UpdateView):
    model = InvestigationType


class InvestigationTypeDeleteView(generic.DeleteView):
    model = InvestigationType

###########
# Project #
###########

class ProjectListView(generic.ListView):
    model = Project


class ProjectCreateView(generic.CreateView):
    model = Project
    fields = '__all__'


class ProjectDetailView(generic.DetailView):
    model = Project


class ProjectUpdateView(generic.UpdateView):
    model = Project


class ProjectDeleteView(generic.DeleteView):
    model = Project

################
# Element Type #
################

class ElementTypeListView(generic.ListView):
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


class ElementTypeDetailView(generic.DetailView):
    model = ElementType


class ElementTypeUpdateView(generic.UpdateView):
    model = ElementType


class ElementTypeDeleteView(generic.DeleteView):
    model = ElementType



############################
# Element Field Descriptor #
############################

class ElementFieldDescriptorListView(generic.ListView):
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

class ElementListView(generic.ListView):
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

class ElementCharFieldValueListView(generic.ListView):
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

