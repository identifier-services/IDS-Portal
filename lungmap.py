import csv
import sys
import os

def split_and_link(path):
    with open(path, 'r') as flat_file:
        reader = csv.DictReader(flat_file, delimiter=',')
        fieldnames = reader.fieldnames

        elements = []

        specimen_fields = [
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
        ]

        elements.append({
            'name': 'specimen',
            'fields': specimen_fields,
            'parents': []
        })

        chunk_fields = [
            'DirectionSection',
            'SectionThickness',
            'TotalSets',
            'Highlight',
            'Rotate',
            'Section',
            'Slide',
            'Set',
        ]

        elements.append({
            'name': 'chunk',
            'fields': chunk_fields,
            'parents': ['specimen']
        })

        probe_fields = [
            'AccessionNumber',
            'GeneSymbol',
            'PrimerForward',
            'PrimerReverse',
            'TemplateSequence',
            'ProbeID',
        ]

        elements.append({
            'name': 'probe',
            'fields': probe_fields,
            'parents': []
        })

        process_fields = [
            'Protocol',
        ]

        elements.append({
            'name': 'process',
            'fields': process_fields,
            'parents': ['probe','chunk']
        })

        image_fields = [
            'URL',
            'FileName',
            'FilePath',
        ]

        elements.append({
            'name': 'image',
            'fields': image_fields,
            'parents': ['chunk', 'image']
        })

        unique_row_sets = dict.fromkeys(fieldnames)
        for k in unique_row_sets.keys():
            unique_row_sets[k] = []

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
