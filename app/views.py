# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import generic

from .models import InvestigationType, Project, ElementType


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


class InvestigationTypeDetailView(generic.DetailView):
    model = InvestigationType

###########
# Project #
###########

class ProjectListView(generic.ListView):
    model = Project


class ProjectDetailView(generic.DetailView):
    model = Project

###############
# Element Type #
###############

class ElementTypeListView(generic.ListView):
    model = ElementType


class ElementTypeDetailView(generic.DetailView):
    model = ElementType
