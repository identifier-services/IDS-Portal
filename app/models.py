# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse


class InvestigationType(models.Model):
    """Model describing the types of projects that may be instantiated."""

    #############
    # Attributes
    #############

    name = models.CharField(max_length=200, 
        help_text="Enter a unique name for this investigation type.",
        unique=True)
    description = models.TextField(max_length=1000, 
        help_text="Enter a brief description of this type of project.",
        blank=True)

    ###############
    # Foreign Keys
    ###############

    # N/A

    ##########
    # Methods
    ##########

    def get_parent_types(self):
        return map(lambda x: x.related_model, filter(lambda x: type(x) == models.ForeignKey, self._meta.get_fields())) 

    def get_child_types(self):
        return map(lambda x: x.related_model, filter(lambda x: type(x) == models.ManyToOneRel, self._meta.get_fields())) 


    def get_absolute_url(self):
        return reverse('app:investigation_type_detail', args=[str(self.id)])

    def __str__(self):
        return self.name 

    #######
    # Meta
    #######

    # N/A


class Project(models.Model):
    """Model representing an individual research project."""

    #############
    # Attributes
    #############

    #TODO: should project name be unique globally? per user?
    name = models.CharField(max_length=200, 
        help_text="Enter a name for this project.")
    description = models.TextField(max_length=1000, 
        help_text="Enter a brief description of this project.",
        blank=True)

    ###############
    # Foreign Keys
    ###############

    # InvestigationType
    investigation_type = models.ForeignKey(InvestigationType, on_delete=models.CASCADE) 

    # Creator

    ##########
    # Methods
    ##########

    def get_parent_types(self):
        return map(lambda x: x.related_model, filter(lambda x: type(x) == models.ForeignKey, self._meta.get_fields())) 

    def get_child_types(self):
        return map(lambda x: x.related_model, filter(lambda x: type(x) == models.ManyToOneRel, self._meta.get_fields())) 

    def get_absolute_url(self):
        return reverse('app:project_detail', args=[str(self.id)])

    def __str__(self):
        return self.name 

    #######
    # Meta
    #######

    # N/A


class ElementType(models.Model):
    """Model describing the types of entities that may be instantiated 
    per investigation type."""

    _parent_type = InvestigationType

    #############
    # Attributes
    #############

    #TODO: should element type name be unique globally? per investigation type?
    name = models.CharField(max_length=200, 
        help_text="Enter a name for this type of element.")
    description = models.TextField(max_length=1000, 
        help_text="Enter a brief description of this type of element.",
        blank=True)

    ###############
    # Foreign Keys
    ###############

    investigation_type = models.ForeignKey(InvestigationType, on_delete=models.CASCADE) 

    ##########
    # Methods
    ##########

    @classmethod
    def get_parent_type(cls):
        return cls._parent_type

    def get_absolute_url(self):
        return reverse('app:element_type_detail', args=[str(self.id)])

    def __str__(self):
        return self.name 

    #######
    # Meta
    #######

    # N/A


class Element(models.Model):
    """Model representing an individual element."""

    #############
    # Attributes
    #############

    #TODO: should element name be unique globally? per project instance?
    name = models.CharField(max_length=200, 
        help_text="Enter a name for this element instance.")
    description = models.TextField(max_length=1000, 
        help_text="Enter a brief description of this element instance.",
        blank=True)

    ###############
    # Foreign Keys
    ###############

    element_type = models.ForeignKey(ElementType, on_delete=models.CASCADE) 
    project = models.ForeignKey(Project, on_delete=models.CASCADE) 

    ##########
    # Methods
    ##########

    def get_parent_type(self):
        return None

    def get_absolute_url(self):
        return reverse('app:element_detail', args=[str(self.id)])

    def __str__(self):
        return self.name 

    #######
    # Meta
    #######

    # N/A


class ElementFieldDescriptor(models.Model):
    """Model describes an attribute of an element."""

    #############
    # Attributes
    #############

    label = models.CharField(max_length=200, 
        help_text="Enter a label for this field.")
    help_text = models.TextField(max_length=1000, 
        help_text="Enter help text for this field.",
        blank=True)
    #TODO: value_type = models. ...
    required = models.BooleanField(default=False, help_text="Is this a required field?")

    ###############
    # Foreign Keys
    ###############

    element_type = models.ForeignKey(ElementType, on_delete=models.CASCADE) 

    ##########
    # Methods
    ##########

    def get_parent_type(self):
        return None

    def get_absolute_url(self):
        return reverse('app:element_field_descriptor_detail', args=[str(self.id)])

    def __str__(self):
        return self.label

    #######
    # Meta
    #######

    # N/A


class AbstractElementFieldValue(models.Model):
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
    """Element CharField attribute value."""

    #############
    # Attributes
    #############

    # inherited

    ###############
    # Foreign Keys
    ###############

    # Element - inherited

    ##########
    # Methods
    ##########

    def get_absolute_url(self):
        return reverse('app:element_char_field_value_detail', args=[str(self.id)])

    def __str__(self):
        return str(self.value)

    #######
    # Meta
    #######

    # N/A

    pass


class ElementTextFieldValue(AbstractElementFieldValue):
    """Element CharField attribute value."""

    #############
    # Attributes
    #############

    value = models.TextField(max_length=1000, blank=True)

    ###############
    # Foreign Keys
    ###############

    # Element - inherited

    ##########
    # Methods
    ##########

    # N/A

    #######
    # Meta
    #######

    # N/A

    pass


class ElementDateFieldValue(AbstractElementFieldValue):
    """Element CharField attribute value."""

    #############
    # Attributes
    #############

    # N/A

    ###############
    # Foreign Keys
    ###############

    # Element - inherited

    ##########
    # Methods
    ##########

    # N/A

    #######
    # Meta
    #######

    # N/A

    pass


class ElementURLFieldValue(AbstractElementFieldValue):
    """Element CharField attribute value."""

    #############
    # Attributes
    #############

    # N/A

    ###############
    # Foreign Keys
    ###############

    # Element - inherited

    ##########
    # Methods
    ##########

    # N/A

    #######
    # Meta
    #######

    # N/A

    pass
