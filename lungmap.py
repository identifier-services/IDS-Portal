import csv
import sys
import os

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
            'parents': ['chunk', 'image'],
            'values': [],
        })

        # create and niitialize dict of lists
        unique_row_sets = dict.fromkeys(fieldnames)
        for k in unique_row_sets.keys():
            unique_row_sets[k] = []

        # iterate through each row in csv
        for row in reader:
            print "----- row ------"
            # for each row, iterate through element defs    
            for element in elements:
                # print element name and element values (in dict key value pairs)
                print element['name'], ':', [{x[0]:x[1]} for x in row.items() if x[0] in element['fields']]
                print
                # # same, but with sets or tuples maybe, instead of dictionary k,v pairs
                # print element['name'], ':', filter(lambda x, y=element['fields']: x[0] in y, row.items())


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
