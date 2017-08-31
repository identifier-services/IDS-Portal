import csv
import sys
import os

def split_and_link(path):
    with open(path, 'r') as flat_file:
        reader = csv.DictReader(flat_file, delimiter=',')
        fieldnames = reader.fieldnames
        unique_values = dict.fromkeys(fieldnames)
        for k in unique_values.keys():
            unique_values[k] = set()

        # chunks are related to a specimen through SpecimenID
        process_application_instances = []
        # PAIs have probes and chunks as input, related through ProbeID and ... chunkid?
        # ChunkID = SpecimenID + Slide + Section
        # related to PAI through ... processID = probeid+chunkid

        elements = []

        # specimen_fields = [
        #     'Species',
        #     'Age',
        #     'SpecimenID',
        #     'Strain',
        #     'Genotype',
        #     'Sex',
        #     'EmbeddingSource',
        #     'DissectionTime',
        #     'PreperationMethod',
        #     'TotalSets',
        # ]

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

        # pk = SpecimenID, no fk

        # chunk_fields = [
        #     'SpecimenID',
        #     'SectionThickness',
        #     'DirectionSection',
        #     'Set',
        #     'Slide',
        #     'Section',
        # ] # Relate to specimen (join with SpecimenID)

        chunk_fields = [
            'DirectionSection',
            'SectionThickness',
            'TotalSets',
            'Highlight',
            'Rotate',
            'Section',
            'Slide',
            'Set',
            # 'SpecimenID'
        ]

        elements.append({
            'name': 'chunk',
            'fields': chunk_fields,
            'parents': ['specimen']
        })

        # add a new field, ChunkID, fk = specimen__SpecimenID

        # probe_fields = [
        #     'GenSymbol',
        #     'ProbeID',
        #     'AccessionNumber',
        #     'TemplateSequence',
        #     'PrimerForward',
        #     'PrimerReverse',
        # ]

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

        # pk = ProbeID

        # process_fields = [
        #     'Protocol',
        #     'ProbeID',
        #     'ChunkID?',
        # ] # Relate to Probe and Chunk (usually 1:1 but one probe or chunk may have many processes)

        process_fields = [
            'Protocol',
            i#'ProbeID', # probe__ProbeID
            #'chunk__ChunkID',
        ]

        elements.append({
            'name': 'process',
            'fields': process_fields,
            'parents': ['probe','chunk']
        })

        # add a field: 'ProcessID' as pk, fk: probe__ProbeID, chunk__SpecimenID -or- chunk__ChunkID

        # image_fields = [
        #     'URL',
        #     'FileName',
        #     'FilePath',
        #     'Highlight',
        # ] # Relate to Chunk through unique Process

        image_fields = [
            'URL',
            'FileName',
            'FilePath',
            # 'chunk__ChunkID',
            # 'ImageID',
        ]

        elements.append({
            'name': 'image',
            'fields': image_fields,
            'parents': ['chunk', 'image']
        })

        # add ImageID as pk

        # [(1, 'DirectionSection'), (1, 'EmbeddingSource'), (1, 'FilePath'), (1, 'Genotype'), (1, 'PreparationMethod'), (1, 'Protocol'), (1, 'SectionThickness'), (1, 'Species'), (1, 'Strain'), (1, 'TotalSets'), (2, 'Highlight'), (2, 'Sex'), (3, 'TissueType'), (4, 'Age'), (4, 'Rotate'), (4, 'Section'), (5, 'DissectionTime'), (5, 'Slide'), (8, 'Set'), (12, 'AccessionNumber'), (12, 'GeneSymbol'), (12, 'PrimerForward'), (12, 'PrimerReverse'), (12, 'ProbeID'), (12, 'TemplateSequence'), (16, 'SpecimenID'), (223, 'URL'), (238, 'FileName')]

        for row in reader:
            for k, v in row.items():
                unique_values[k].add(v)

        lengths = []

        for k, v in unique_values.items():
            lengths.append((len(v), k))

        # print 'field count: %s' % len(lengths)

        lengths.sort()
        # print lengths

        unique_row_sets = dict.fromkeys(fieldnames)
        for k in unique_row_sets.keys():
            unique_row_sets[k] = []

        

if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        print 'usage:\n$ python explode.py [filename]'
        sys.exit(0)
    split_and_link(args[1])
