# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


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

    # N/A

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

    # N/A

    #######
    # Meta
    #######

    # N/A


class EntityType(models.Model):
    """Model describing the types of entities that may be instantiated 
    per investigation type."""

    #############
    # Attributes
    #############

    #TODO: should entity type name be unique globally? per investigation type?
    name = models.CharField(max_length=200, 
        help_text="Enter a name for this type of entity.")
    description = models.TextField(max_length=1000, 
        help_text="Enter a brief description of this type of entity.",
        blank=True)

    ###############
    # Foreign Keys
    ###############

    investigation_type = models.ForeignKey(InvestigationType, on_delete=models.CASCADE) 

    ##########
    # Methods
    ##########

    # N/A

    #######
    # Meta
    #######

    # N/A


class Entity(models.Model):
    """Model representing an individual entity."""

    #############
    # Attributes
    #############

    #TODO: should entity name be unique globally? per project instance?
    name = models.CharField(max_length=200, 
        help_text="Enter a name for this entity instance.")
    description = models.TextField(max_length=1000, 
        help_text="Enter a brief description of this entity instance.",
        blank=True)

    ###############
    # Foreign Keys
    ###############

    entity_type = models.ForeignKey(EntityType, on_delete=models.CASCADE) 
    project = models.ForeignKey(Project, on_delete=models.CASCADE) 

    ##########
    # Methods
    ##########

    # N/A

    #######
    # Meta
    #######

    # N/A


class EntityFieldDescriptor(models.Model):
    """Model describes an attribute of an entity."""

    #############
    # Attributes
    #############

    label = models.CharField(max_length=200, 
        help_text="Enter a label for this field.")
    help_text = models.TextField(max_length=1000, 
        help_text="Enter help text for this field.",
        blank=True)
    #TODO: value_type = models. ...
    required = models.BooleanField(default=False, "Is this a required field?")

    ###############
    # Foreign Keys
    ###############

    entity_type = models.ForeignKey(EntityType, on_delete=models.CASCADE) 

    ##########
    # Methods
    ##########

    # N/A

    #######
    # Meta
    #######

    # N/A


class AbstractEntityFieldValue(models.Model):
    """Abstract class for various types of entity field values"""

    #############
    # Attributes
    #############

    # N/A

    ###############
    # Foreign Keys
    ###############

    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)

    ##########
    # Methods
    ##########

    # N/A

    #######
    # Meta
    #######

    class Meta:
        abstract = True


class EntityCharFieldValue(AbstractEntityFieldValue):
    """Entity CharField attribute value."""

    #############
    # Attributes
    #############

    value = models.CharField(max_length=200)

    ###############
    # Foreign Keys
    ###############

    # Entity - inherited

    ##########
    # Methods
    ##########

    # N/A

    #######
    # Meta
    #######

    # N/A

    pass


class EntityTextFieldValue(AbstractEntityFieldValue):
    """Entity CharField attribute value."""

    #############
    # Attributes
    #############

    value = models.TextField(max_length=1000, blank=True)

    ###############
    # Foreign Keys
    ###############

    # Entity - inherited

    ##########
    # Methods
    ##########

    # N/A

    #######
    # Meta
    #######

    # N/A

    pass


class EntityDateFieldValue(AbstractEntityFieldValue):
    """Entity CharField attribute value."""

    #############
    # Attributes
    #############

    # N/A

    ###############
    # Foreign Keys
    ###############

    # Entity - inherited

    ##########
    # Methods
    ##########

    # N/A

    #######
    # Meta
    #######

    # N/A

    pass


class EntityURLFieldValue(AbstractEntityFieldValue):
    """Entity CharField attribute value."""

    #############
    # Attributes
    #############

    # N/A

    ###############
    # Foreign Keys
    ###############

    # Entity - inherited

    ##########
    # Methods
    ##########

    # N/A

    #######
    # Meta
    #######

    # N/A

    pass
