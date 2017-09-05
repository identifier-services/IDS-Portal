import csv
import sys
import os
import uuid
import pprint

def split_and_link(path):
    with open(path, 'r') as flat_file:
        reader = csv.DictReader(flat_file, delimiter=',')
        fieldnames = reader.fieldnames

        elements = []

        ############
        # specimen #
        ############

        elements.append({
            'name': 'specimen',
            'fields': [
                'EmbeddingSource',
                'Genotype',
                'PreparationMethod',
                'Species',
                'Strain',
                'TotalSets',
                'Sex',
                'TissueType',
                'Age',
                'DissectionTime',
                'SpecimenID'
            ],
            'parents': [],
            'values': [],
        })

        #########
        # chunk #
        #########

        elements.append({
            'name': 'chunk',
            'fields': [
                'DirectionSection',
                'SectionThickness',
                'TotalSets',
                'Highlight',
                'Rotate',
                'Section',
                'Slide',
                'Set',
            ],
            'parents': ['specimen'],
            'values': [],
        })

        #########
        # probe #
        #########

        elements.append({
            'name': 'probe',
            'fields': [
                'AccessionNumber',
                'GeneSymbol',
                'PrimerForward',
                'PrimerReverse',
                'TemplateSequence',
                'ProbeID',
            ],
            'parents': [],
            'values': [],
        })

        ###########
        # process #
        ###########

        elements.append({
            'name': 'process',
            'fields': [
                'Protocol',
            ],
            'parents': ['probe','chunk'],
            'values': [],
        })

        #########
        # image #
        #########

        elements.append({
            'name': 'image',
            'fields': [
                'URL',
                'FileName',
                'FilePath',
            ],
            'parents': ['process'],
            'values': [],
        })

        # i'm sure what follows could be done more efficiently
        # maybe i should import sqlite and build/query db

        rows = []
        for row in reader:
            rows.append(row)

        unique_element_strings = []

        for element in elements:
            field_names = element['fields']
            element_type = element['name']
            pk_name = '__%sID' % (element_type.title())
            pk_id = None
            element_values = {}
            for row in rows:
                for field_name in field_names:
                    element_values.update({field_name: row[field_name]})
                if not str(element_values) in unique_element_strings:
                    unique_element_strings.append(str(element_values))
                    pk_id = str(uuid.uuid4())
                    element_values.update({pk_name: pk_id})
                    element['values'].append(element_values)
                row.update({pk_name: pk_id})

        # for element in elements:
        #     print
        #     print '---', element['name'], '---', element['values']
        #     print

        for element in elements:
            element_type = element['name']
            primary_key = '__%sID' % (element_type.title())
            parents = []
            for parent in element['parents']:
                parents.append({'name': parent, 'key': '__%sID' % parent.title()})
            for value in element['values']:
                pk_id = value.get(primary_key)
                for row in rows:
                    row_pk = row.get(primary_key)
                    if row_pk == pk_id:
                        for parent in parents:
                            name = parent['name']
                            key = parent['key']
                            fk = row.get(key)
                            if fk:
                                value.update({'%s%s' % (name, key): fk})
                        break


        for element in elements:
            print
            print '---', element['name'], '---'
            pprint.pprint(element['values'])
            print

if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        print 'usage:\n$ python explode.py [filename]'
        sys.exit(0)
    split_and_link(args[1])

## count of unique values, don't know if useful
# DirectionSection 1
# EmbeddingSource 1
# FilePath 1
# Genotype 1
# PreparationMethod 1
# Protocol 1
# SectionThickness 1
# Species 1
# Strain 1
#  TotalSets 1
# Highlight 2
# Sex 2
# TissueType 3
# Age 4
# Rotate 4
# Section 4
# DissectionTime 5
# Slide 5
# Set 8
# AccessionNumber 12
# GeneSymbol 12
# PrimerForward 12
# PrimerReverse 12
# ProbeID 12
# TemplateSequence 12
# SpecimenID 16
# URL 223
# FileName 238
