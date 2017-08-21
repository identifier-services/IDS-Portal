# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.views import generic

from zipfile import ZipFile
import csv

from app.models import InvestigationType, Project, ElementType


#############
# Home Page #
#############

def index(request):
    """home page"""
    return render (request, 'bulk/index.html', context={})

##########
# Upload #
##########

def upload(request):
    """bulk uploads"""

    ########
    # POST #
    ########

    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        zf = ZipFile(myfile)
        for filename in zf.namelist():
            data = zf.read(filename).split('\n')
            reader = csv.DictReader(data, delimiter=str('\t'))
            for row in reader:
                print row
#    * # TODO
#      * user uploads zip file
#        * specifies project name
#          * same name as zip file?
#        * specifies investigation type
#          * existing or new
#      * app extracts csv files
#      * app instantiates csv.DictReader for each csv file
#      * app reads (next) each line into separate list for each csv file
#      * app processes lists
#        * for each list:
#          * if not existing, app creates element type
#            * element type is related to investigation type
#            * for each header:
#              * if not existing, app creates field_descriptor
#                * fd is related to element type and investigation type
#                * TODO: add description and value-type
#            * for each line:
#              * app creates new element
#                * element is assocaited to the project, entity type
#              * app iterates through headers
#                * for each header:
#                  * app reads value from dict
#                  * app creates new [char]fieldvalue (or whatever)
#                    * fieldavalue is related to element, fielddescriptor
#                * special headers:
#                  * some headers will define relationships
#                    * rather than attributes
#                    * relationships:
#                      * [x] belongs to? is part of? contained by?
#                      * [x] input of? output of?
#                      * [ ] has inputs? has outputs?
#                      * [ ] precursor to? successor of?
#                      * [ ] next? previous?
#                      * [?] has output type? has input type?
#                        * 'suggest' model?
#              * note: i think we need to create all the object before we create relationships between them.
        return render (request, 'bulk/upload.html', context={})

    #######
    # GET #
    #######

    return render (request, 'bulk/upload.html', context={})

############
# Download #
############

def download(request):
    """bulk downloads"""
    return render (request, 'bulk/download.html', context={})
