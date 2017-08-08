# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import *


@admin.register(InvestigationType)
class InvestigationTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(EntityType)
class EntityTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    pass


@admin.register(EntityFieldDescriptor)
class EntityFieldDescriptorAdmin(admin.ModelAdmin):
    pass


@admin.register(EntityCharFieldValue)
class EntityCharFieldValueAdmin(admin.ModelAdmin):
    pass


@admin.register(EntityTextFieldValue)
class EntityTextFieldValueAdmin(admin.ModelAdmin):
    pass


@admin.register(EntityDateFieldValue)
class EntityDateFieldValueAdmin(admin.ModelAdmin):
    pass


@admin.register(EntityURLFieldValue)
class EntityURLFieldValueAdmin(admin.ModelAdmin):
    pass
