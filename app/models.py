# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, transaction
from django.urls import reverse

import uuid
import re
import yaml
import csv
import logging

logger = logging.getLogger(__name__)

def snake(name):
    """
    Takes camelcase string, returns string in snake case.
    https://stackoverflow.com/a/12867228
    """
    return re.sub('(?!^)([A-Z]+)', r'_\1', name).lower()


class Base(object):
    """
    Provides methods for various abstract model classes.
    """ # I think it doesn't follow good practice through.

    # TODO: add is_public (queries project)
    # TODO: add owner (queries project)

    @classmethod
    def get_parent_types(self):
        fields = self._meta.get_fields()
        foreign_keys = filter(lambda x: type(x) == models.ForeignKey, fields)
        parent_types = []

        for foreign_key in foreign_keys:
            parent = getattr(self, foreign_key.name)
            parent_types.append({
                'field_name': foreign_key.name,
                'class': parent.field.related_model,
            })

        return parent_types

    def get_parent_relations(self):
        fields = self._meta.get_fields()
        foreign_keys = filter(lambda x: type(x) == models.ForeignKey, fields)
        parents = []
        for foreign_key in foreign_keys:
            parent = getattr(self, foreign_key.name)
            parents.append({
                'verbose_name': parent._meta.verbose_name,
                'object': parent,
            })

        return parents

    def get_child_relations(self):
        fields = self._meta.get_fields()
        many_to_ones = filter(lambda x: type(x) == models.ManyToOneRel, fields)
        child_relations = []
        for many_to_one in many_to_ones:        
            rm = getattr(self, many_to_one.get_accessor_name())

            child_relations.append({
                'type_name': many_to_one.related_model._meta.verbose_name,
                'objects': rm.all(),
                'create_url': many_to_one.related_model.get_create_url(),
            })

        return child_relations

    def get_fields(self):
        fields = filter(lambda x: (not x.auto_created and not x.related_model),
            self._meta.get_fields())

        field_list = []
        for field in fields:
            field_list.append({
                'label': field.verbose_name,
                'value': getattr(self, field.name),
            })

        return field_list

    def get_absolute_url(self):
        route = 'app:%s_detail' % snake(self.__class__.__name__)
        return reverse(route, args=[str(self.id)])

    @classmethod
    def get_create_url(cls):
        route = 'app:%s_create' % snake(cls.__name__)
        return reverse(route)

    def __str__(self):
        return self.name 


class AbstractModel(Base, models.Model):
    """
    Abstract model class, provides standard name and description fields, as
    well as methods return related objects. Subclasses will need to specify 
    foreign key fields.
    """

    def __init__(self, *args, **kwargs):
        super(AbstractModel, self).__init__(*args, **kwargs)

        # this is really hacky, for one reason, because it doesn't
        # set the new help_text until after the first time the
        # user sees it. leaving it for now though...

        verbose_name = self._meta.verbose_name
        help_text = 'Enter a name for this %s.' % verbose_name
        try:
            self._meta.get_field('name').help_text = help_text
        except Exception as e:
            # logger.debug(e)
            print e

        help_text = 'Enter a description for this %s.' % verbose_name
        try:
            self._meta.get_field('description').help_text = help_text
        except Exception as e:
            # logger.debug(e)
            print e

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=200, 
        help_text="Enter a name.", blank=True)

    description = models.TextField(max_length=1000, 
        help_text="Enter a description.", blank=True)

    class Meta:
        abstract = True


class Node(object):
    def __init__(self):
        self.name = ''
        self.left = []
        self.right = []
        self.obj = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'graph node: %s, |left| = %s, |right| = %s' % (
            self.name, str(len(self.left)), str(len(self.right)))


class InvestigationType(AbstractModel):
    """Model describing the types of projects that may be instantiated."""

    definition_file = models.FileField('definition file(s)', upload_to='documents/%Y/%m/%d/', 
        blank=True, null=True)

    def _build_graph(self, root):
        fk_type_rels = ['PART','ISIN','ISOU']
        temp_list = root.right
        for node in temp_list:
            for parent_rel in node.obj.forward_relationship_defs.filter(
                rel_type_abbr__in=fk_type_rels):
                parent = parent_rel.target
                parent_node = next(iter(
                    filter(lambda a,b=parent: a.obj==b, temp_list)))
                if not parent_node:
                    continue
                if parent_node not in node.left:
                    node.left.append(parent_node)
                if node not in parent_node.right:
                    parent_node.right.append(node)
                if node in root.right:
                    root.right.remove(node)
                if root in node.left:
                    node.left.remove(root)

    @property
    def graph(self):
        root = Node()
        root.name = 'Investigation Type: %s' % self.name
        root.obj = self

        for element_type in ElementType.objects.filter(investigation_type=self):
            n = Node()
            n.name = element_type.name
            n.left.append(root)
            root.right.append(n)
            n.obj = element_type

        self._build_graph(root)

        return root

    # def _build_dep_list(self, node):
    #     print node
    #     for child in node.right:
    #         self._build_dep_list(child)

    # @property
    # def dependency_list(self):
    #     return self._build_dep_list(self.graph)
        

    def save(self, *args, **kwargs):
        super(InvestigationType, self).save(*args, **kwargs)

        # TODO: move this code somewhere else, and don't run it in the django process!

        definitions = []
        try:
            definitions = [x for x in yaml.load_all(self.definition_file.file)]
        except Exception as e:
            logger.debug(e)

        for definition in definitions:
            name = definition.get('name', '')
            description = definition.get('description', '')
            fields = definition.get('fields', [])
        
            elem_type = ElementType(
                name=name, 
                description=description,
                investigation_type=self
            )

            elem_type.save()

            for field in fields:
                val_type = field.get('value type', '')
                value_type_abbr = ElementFieldDescriptor.CHAR

                try:
                    value_type_abbr = filter(
                        lambda x, y=val_type: x[1]==y, 
                        ElementFieldDescriptor.VALUE_TYPE_CHOICES
                    )[0][0]
                except Exception as e:
                    logger.debug(e)

                elem_field_descr = ElementFieldDescriptor(
                    label=field.get('name', ''),
                    help_text=field.get('description', ''),
                    value_type_abbr=value_type_abbr,
                    required=field.get('required', False),
                    element_type=elem_type,
                )

                elem_field_descr.save()

        for definition in definitions:
            rels = definition.get('rels', [])
        
            for rel in rels:
                card = rel.get('cardinality', '')
                card_abbr = RelationshipDefinition.ONE #default

                try:
                    card_abbr = filter(
                        lambda x, y=card: x[1]==y, 
                        RelationshipDefinition.CARDINALITIES)[0][0]
                except Exception as e:
                    logger.debug(e)

                rel_type = rel.get('type', '')
                rel_type_abbr = RelationshipDefinition.PART #default

                try:
                    rel_type_abbr = filter(
                        lambda x, y=rel_type: x[1]==y, 
                        RelationshipDefinition.RELATIONSHIP_TYPES)[0][0]
                except Exception as e:
                    logger.debug(e)

                source_name = definition.get('name', '')
                source = ElementType.objects.get(investigation_type=self, 
                    name__exact=source_name)
                target_name = rel.get('target', '')
                target = ElementType.objects.get(investigation_type=self, 
                    name__exact=target_name)

                rel_def = RelationshipDefinition(
                    source=source,
                    target=target,
                    rel_type_abbr=rel_type_abbr,
                    card_abbr=card_abbr
                )

                print source, rel_type_abbr, rel_type,

                rel_def.save()

    class Meta:
        verbose_name = "investigation type"


class Project(AbstractModel):
    """Model representing an individual research project."""

    investigation_type = models.ForeignKey(InvestigationType, on_delete=models.CASCADE) 

    archive = models.FileField('bulk upload', upload_to='documents/%Y/%m/%d/', 
        blank=True, null=True)

    # TODO: add fk to owner/creator (auth.user)
    # TODO: add many-to-many to collaborators
        
    def save(self, *args, **kwargs):
        super(Project, self).save(*args, **kwargs)

        # TODO: create new investigation_type if user does not select existing
        if not self.investigation_type or not self.archive:
            return

        # TODO: handle zip of multiple csv, or just multiple csv uploads
        archive_file = self.archive.file
        if not archive_file.name.split('.')[-1] == 'csv':
            return
        
        reader = csv.DictReader(archive_file, 
            delimiter=str(u',').encode('utf-8'))

        rows = []
        # read entire csv into memory, could be prohibitive for huge sheets
        for row in reader:
            rows.append(row)

        # get list of elements for this investigation type
        element_types = ElementType.objects.filter(
            investigation_type=self.investigation_type)

        # we're going to stick values in here the first time we see them
        # if values are not unique, we do not create a new element
        unique_element_strings = set()

        # temporarily hold field values
        field_values = {}

        # the following seems fairly inefficient, but it works to create 
        # unique elements (relationships between elements are established
        # in a subsequent step).
        # - loop though each element type definition
        # - for each element type, loop through each row of csv
        # - for each row, loop through each (element type) field
        # - get the field value from the csv and add to a dictionary
        # - use complete list of k,v pairs to create a new element string
        # - if element string found in set of unique values continue, else
        # - save element to db and store string in unique set  
        for element_type in element_types:

            # get field defs for this element type
            field_descriptors = element_type.elementfielddescriptor_set.all()

            # clear previous element's values
            field_values.clear()

            # loop through all rows in the csv
            for row in rows:

                # grab all field values for this element in this row
                for field_descriptor in field_descriptors:
                    field_name = field_descriptor.label
                    field_value = row.get(field_name)
                    if field_value:
                        field_values.update({field_name: field_value})

                # we need a hashable object to check for uniqueness
                value_string = str(field_values)

                # check for uniqueness
                if value_string in unique_element_strings:
                    continue
                    
                with transaction.atomic():
                    # create a new element
                    new_element = Element(id=uuid.uuid4(),
                        element_type=element_type, project=self)

                    # run through all the field descriptors again to create
                    # the new values
                    for field_descriptor in field_descriptors:
                        field_value = field_values[field_descriptor.label]

                        new_value = field_descriptor.value_type(
                            value=field_value,
                            element_field_descriptor=field_descriptor,
                            element=new_element)
                        new_value.save()

                    # add value string to set
                    unique_element_strings.add(value_string)

                    # we need a display field
                    # TODO: this display field issue needs a lot more thought! 
                    #   and changes to the model, we don't need name/descr on
                    #   elements, we just need to know which field is the
                    #   display field
                    if field_values:
                        first_value = next(iter(field_values.items()))
                        display_value = '%s: %s - %s' % (
                            element_type.name.title(),
                            first_value[0],
                            first_value[1],
                        )
                        new_element.name=display_value
                        new_element.save()
                    row.update({'__%s_ID'%new_element.name:new_element.pk})

        import pdb; pdb.set_trace()


class ElementType(AbstractModel):
    """Model describing the types of entities that may be instantiated 
    per investigation type."""

    investigation_type = models.ForeignKey(InvestigationType, on_delete=models.CASCADE) 

    # relationships = models.ManyToManyField('self',
    #     through='RelationshipDefinition', symmetrical=False, 
    #     related_name='related_to')

    class Meta:
        verbose_name = "element type"


class ElementFieldDescriptor(Base, models.Model):
    """Model describes an attribute of an element."""

    #############
    # Attributes
    #############

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    label = models.CharField(max_length=200, 
        help_text="Enter a label for this field.", blank=True)

    help_text = models.TextField(max_length=1000, 
        help_text="Enter help text for this field.",
        blank=True)

    CHAR = 'CHR'
    TEXT = 'TXT'
    INT = 'INT'
    FLOAT = 'FLT'
    DATE = 'MDY'
    URL = 'URL'
    REL = 'REL'
    VALUE_TYPE_CHOICES = (
        (CHAR, 'short text'),
        (TEXT, 'long text'),
        (INT, 'integer'),
        (FLOAT, 'real number'),
        (DATE, 'date'),
        (URL, 'url'),
        (REL, 'relation'),
    )

    value_type_abbr = models.CharField(
        "value type",
        max_length=3,
        choices=VALUE_TYPE_CHOICES,
        default=CHAR,
    )

    required = models.BooleanField(default=False, 
        help_text="Is this a required field?")

    ###############
    # Foreign Keys
    ###############

    element_type = models.ForeignKey(ElementType, on_delete=models.CASCADE) 

    #############
    # Properties    
    #############

    @property
    def value_type_map(self):
        mapping = {                                                        
            self.CHAR: ElementCharFieldValue,
            self.TEXT: ElementTextFieldValue,
            self.INT: ElementIntFieldValue,
            self.FLOAT: ElementFloatFieldValue,
            self.DATE: ElementDateFieldValue,
            self.URL: ElementUrlFieldValue,
            self.REL: ElementCharFieldValue, # TODO: add rel field 
        } 
        return mapping

    @property
    def value_type(self):
        return self.value_type_map[self.value_type_abbr]

    @property
    def verbose_value_type(self):
        try:
            return filter(lambda x, y=self.value_type_abbr: x[0]==y,self.VALUE_TYPE_CHOICES)[0][1]
        except Exception as e:
            logger.debug(e)

        return self.value_type_abbr

    ##########
    # Methods
    ##########

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = "element field descriptor"


class RelationshipDefinition(Base, models.Model):
    """Describes a the relationships that may exist between element types."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.ForeignKey(ElementType, on_delete=models.CASCADE, 
        related_name='forward_relationship_defs')
    target = models.ForeignKey(ElementType, on_delete=models.CASCADE, 
        related_name='reverse_relationship_defs')
    
    ORIG = 'ORIG'
    PART = 'PART'
    ISIN = 'ISIN'
    ISOU = 'ISOU'
    HASI = 'HASI'
    HASO = 'HASO'
    CONT = 'CONT'

    RELATIONSHIP_TYPES = (
        (ORIG, 'is origin of'),
        (PART, 'is part of'),
        (ISIN, 'is input to'),
        (ISOU, 'is output of'),
        (HASI, 'has input'),
        (HASO, 'has output'),
        (CONT, 'contains'),
    )

    rel_type_abbr = models.CharField(
        "relationship type",
        max_length = 4,
        choices = RELATIONSHIP_TYPES,
        default=PART,
    )

    ZERO = 'ZERO'
    ONE = 'ONE'
    ZO = 'ZO'
    MANY = 'MANY'
    OM = 'OM'
    ZOM = 'ZOM'

    CARDINALITIES = (
        (ZERO, 'zero'),
        (ONE, 'one'),
        (ZO, 'zero or one'),
        (MANY, 'many'),
        (OM, 'one or many'),
        (ZOM, 'zero one or many'),
    )

    card_abbr = models.CharField(
        'cardinality',
        max_length = 4,
        choices = CARDINALITIES,
        default=ONE,
    )

    @property
    def verbose_relationship_type(self):
        try:
            return filter(lambda x, y=self.rel_type_abbr: x[0]==y, 
                self.RELATIONSHIP_TYPES)[0][1]
        except Exception as e:
            logger.debug(e)

        return self.rel_type_abbr

    @property
    def verbose_cardinality(self):
        try:
            return filter(lambda x, y=self.card_abbr: x[0]==y, 
                self.CARDINALITIES)[0][1]
        except Exception as e:
            logger.debug(e)

        return self.card_abbr

    def __str__(self):
        return '%s %s %s %s' % (
            self.source.name, 
            self.verbose_relationship_type, 
            self.verbose_cardinality,
            self.target.name
        )


class Element(AbstractModel):
    """Model representing an individual element."""

    element_type = models.ForeignKey(ElementType, on_delete=models.CASCADE) 
    project = models.ForeignKey(Project, on_delete=models.CASCADE) 


class Relationship(Base, models.Model):
    """Relates two elements"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.ForeignKey(Element, on_delete=models.CASCADE, related_name='source_object')
    target = models.ForeignKey(Element, on_delete=models.CASCADE, related_name='target_object')

    def __str__(self):
        return '%s - %s' % (
            self.source.name, 
            self.target.name
        )


class AbstractElementFieldValue(Base, models.Model):
    """Abstract class for various types of element field values"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    ###############
    # Foreign Keys
    ###############

    element = models.ForeignKey(Element, on_delete=models.CASCADE)
    element_field_descriptor = models.ForeignKey(ElementFieldDescriptor, 
        on_delete=models.CASCADE, null=True)

    ##########
    # Methods
    ##########

    def __str__(self):
        return str(self.value)

    #######
    # Meta
    #######

    class Meta:
        abstract = True


class ElementCharFieldValue(AbstractElementFieldValue):
    """Element char field attribute value."""

    value = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.value)

    class Meta:
        verbose_name = 'short text value'


class ElementTextFieldValue(AbstractElementFieldValue):
    """Element text field attribute value."""

    value = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'long text value'


class ElementIntFieldValue(AbstractElementFieldValue):
    """Element CharField attribute value."""

    value = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'integer value'


class ElementFloatFieldValue(AbstractElementFieldValue):
    """Element CharField attribute value."""

    value = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = 'float value'


class ElementDateFieldValue(AbstractElementFieldValue):
    """Element date field attribute value."""

    value = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)

    class Meta:
        verbose_name = 'date value'


class ElementUrlFieldValue(AbstractElementFieldValue):
    """Element CharField attribute value."""

    value = models.URLField(max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = 'url value'


# class ElementRelFieldValue(AbstractElementFieldValue):
#     """Element CharField attribute value."""
# 
#     value = models.CharField(max_length=200, blank=True, null=True)
# 
#     class Meta:
#         verbose_name = 'url'
