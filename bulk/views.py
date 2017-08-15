# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import generic

from app.models import InvestigationType, Project, ElementType


#############
# Home Page #
#############

def index(request):
    """home page"""
    return render (request, 'index.html', context={})

##########
# Upload #
##########

def upload(request):
    """bulk uploads"""
    return render (request, 'upload.html', context={})

############
# Download #
############

def download(request):
    """bulk downloads"""
    return render (request, 'download.html', context={})
