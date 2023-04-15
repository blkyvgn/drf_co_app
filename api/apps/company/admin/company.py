from django.contrib import admin
from django.conf import settings
from api.vendors.base.model import AdminBaseModel
from django.utils.html import format_html
from api.apps.company.models import Company


@admin.register(Company)
class CompanyAdmin(AdminBaseModel):
	list_display = [
		'get_logo',
		'alias', 
		'get_name',
		'is_valid', 
	]
	fieldsets = (
		(None, {
			'fields': (
				('is_valid',), 
				'alias',
				'_name',
				'logo',
				'options',
			)
		}),
	)
	list_filter = [
		'is_valid',
	]
	list_display_links = ('alias',)
	search_fields = ('alias',)
	ordering = ('-created_at',)

	@admin.display(description='Name')
	def get_name(self, obj):
		return obj.name

	@admin.display(description='Logo')
	def get_logo(self, obj):
		return format_html(
			'<img width="60" src="{}" />'.format(
				obj.img_url_or_default('logo', settings.DEFAULT_IMAGE['LOGO'])
			)
		)