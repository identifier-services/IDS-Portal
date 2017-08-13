# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import generic

from .models import Project


def index(request):
    """home page"""
    return render (request, 'index.html', context={})


class ProjectListView(generic.ListView):
    model = Project
