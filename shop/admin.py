# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Publication, PublicationType, Category


class PublicationAdmin(admin.ModelAdmin):
	pass

class PublicationTypeAdmin(admin.ModelAdmin):
	pass

class CategoryAdmin(admin.ModelAdmin):
	pass
admin.site.register(Publication, PublicationAdmin)
admin.site.register(PublicationType, PublicationTypeAdmin)
admin.site.register(Category, CategoryAdmin)