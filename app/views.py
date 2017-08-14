# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import generic

from .models import InvestigationType, Project, EntityType


#############
# Home Page #
#############

def index(request):
    """home page"""
    return render (request, 'index.html', context={})

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
# Entity Type #
###############

class EntityTypeListView(generic.ListView):
    model = EntityType


class EntityTypeDetailView(generic.DetailView):
    model = EntityType
