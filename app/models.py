# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse

import re

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

    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)

        # this is really hacky, for one reason, because it doesn't
        # set the new help_text until after the first time the
        # user sees it. leaving it for now though...

        verbose_name = self._meta.verbose_name
        help_text = 'Enter a name for this %s.' % verbose_name
        self._meta.get_field('name').help_text = help_text

        help_text = 'Enter a description for this %s.' % verbose_name
        self._meta.get_field('description').help_text = help_text

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
            # rm = getattr(self,'%s_set' % many_to_one.name)
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

    name = models.CharField(max_length=200, 
        help_text="Enter a name.", default="N/A")

    description = models.TextField(max_length=1000, 
        help_text="Enter a description.", blank=True)

    #def __init__(self, *args, **kwargs):
    #    super(AbstractModel, self).__init__(*args, **kwargs)

        # this is really hacky, for one reason, because it doesn't
        # set the new help_text until after the first time the
        # user sees it. leaving it for now though...

    #    verbose_name = self._meta.verbose_name
    #    help_text = 'Enter a name for this %s.' % verbose_name
    #    self._meta.get_field('name').help_text = help_text

    #    help_text = 'Enter a description for this %s.' % verbose_name
    #    self._meta.get_field('description').help_text = help_text

    class Meta:
        abstract = True


class InvestigationType(AbstractModel):
    """Model describing the types of projects that may be instantiated."""

    class Meta:
        verbose_name = "investigation type"


class Project(AbstractModel):
    """Model representing an individual research project."""

    investigation_type = models.ForeignKey(InvestigationType, on_delete=models.CASCADE) 


class ElementType(AbstractModel):
    """Model describing the types of entities that may be instantiated 
    per investigation type."""

    investigation_type = models.ForeignKey(InvestigationType, on_delete=models.CASCADE) 

    class Meta:
        verbose_name = "element type"


class Element(AbstractModel):
    """Model representing an individual element."""

    element_type = models.ForeignKey(ElementType, on_delete=models.CASCADE) 
    project = models.ForeignKey(Project, on_delete=models.CASCADE) 


# class ElementFieldDescriptor(models.Model):
class ElementFieldDescriptor(AbstractModel):
    """Model describes an attribute of an element."""

    #############
    # Attributes
    #############

    # label = models.CharField(max_length=200, 
    #     help_text="Enter a label for this field.")
    # help_text = models.TextField(max_length=1000, 
    #     help_text="Enter help text for this field.",
    #     blank=True)
    #TODO: value_type = models. ...

    # def __init__(self, *args, **kwargs):
    #     super(ElementFieldDescriptor, self).__init__(*args, **kwargs)
    #     fields = filter(lambda x: (not x.auto_created and not x.related_model),
    #         self._meta.get_fields())
    #     for field in self._meta.get_fields():
    #         if field.name == 'name':
    #             field.verbose_name = 'label'
    #         elif field.name == 'description':
    #             field.verbose_name = 'help text'

    required = models.BooleanField(default=False, help_text="Is this a required field?")

    ###############
    # Foreign Keys
    ###############

    element_type = models.ForeignKey(ElementType, on_delete=models.CASCADE) 

    ##########
    # Methods
    ##########

    # def get_absolute_url(self):
    #     return reverse('app:element_field_descriptor_detail', args=[str(self.id)])

    # def __str__(self):
    #     return self.label

    class Meta:
        verbose_name = "element field descriptor"


class AbstractElementFieldValue(Base, models.Model):
    """Abstract class for various types of element field values"""

    #############
    # Attributes
    #############

    value = models.CharField(max_length=200, blank=True, null=True)

    ###############
    # Foreign Keys
    ###############

    element = models.ForeignKey(Element, on_delete=models.CASCADE)
    element_field_descriptor = models.ForeignKey(ElementFieldDescriptor, on_delete=models.CASCADE, null=True)

    ##########
    # Methods
    ##########

    def get_parent_type(self):
        return None

    def __str__(self):
        return str(self.value)

    #######
    # Meta
    #######

    class Meta:
        abstract = True


class ElementCharFieldValue(AbstractElementFieldValue):
    """Element char field attribute value."""

    def get_absolute_url(self):
        return reverse('app:element_char_field_value_detail', args=[str(self.id)])

    def __str__(self):
        return str(self.value)

    #######
    # Meta
    #######

    class Meta:
        verbose_name = 'char field value'


class ElementTextFieldValue(AbstractElementFieldValue):
    """Element text field attribute value."""

    class Meta:
        verbose_name = 'text value'


class ElementDateFieldValue(AbstractElementFieldValue):
    """Element date field attribute value."""

    class Meta:
        verbose_name = 'date'


class ElementUrlFieldValue(AbstractElementFieldValue):
    """Element CharField attribute value."""

    class Meta:
        verbose_name = 'url'
