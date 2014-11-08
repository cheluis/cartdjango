# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Publication, PublicationType, Category


class PublicationAdmin(admin.ModelAdmin):
	pass

admin.site.register(Publication, PublicationAdmin)