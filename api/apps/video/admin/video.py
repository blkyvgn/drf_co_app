from django.contrib import admin
from django.conf import settings
from django.utils.translation import get_language
from api.vendors.base.model import AdminBaseModel
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from api.apps.video.models import Video


@admin.register(Video)
class VideoAdmin(AdminBaseModel):

	list_display = [
		'get_thumb',
		'slug', 
		'is_valid', 
		'file'
	]
	fieldsets = (
		(None, {
			'fields': (
				('is_valid',), 
				'slug',
				'thumb',
				'file',
				'alt',
				'company',
			)
		}),
	)
	list_filter = [
		'is_valid',
	]
	list_display_links = ('slug',)
	search_fields = ('slug',)
	ordering = ('-created_at',)

	@admin.display(description='Logo')
	def get_thumb(self, obj):
		return format_html(
			'<img width="80" src="{}" />'.format(
				obj.img_url_or_default('thumb', settings.DEFAULT_IMAGE['PLACEHOLDER'])
			)
		)

	def save_model(self, request, obj, form, change):
		super().save_model(request, obj, form, change)

	def delete_model(self, request, obj, form, change):
		super().delete_model(request, obj, form, change)