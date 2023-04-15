from django.contrib import admin
from django.conf import settings
from django.utils.translation import get_language
from api.vendors.base.model import AdminBaseModel
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from api.apps.blog.models import (
	Article,
	ArticleBody,
)


@admin.register(Article)
class ArticleAdmin(AdminBaseModel):
	def get_queryset(self, request):
		return super().get_queryset(request).\
			select_related('author').select_related('category')

	list_display = [
		'get_thumb',
		'slug', 
		'is_valid', 
		'get_author',
		'get_category'
	]
	fieldsets = (
		(None, {
			'fields': (
				('is_valid',), 
				'slug',
				'thumb',
				'category',
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
	raw_id_fields = ['category',]

	@admin.display(description='Author')
	def get_author(self, obj):
		return obj.author.username

	@admin.display(description='Category')
	def get_category(self, obj):
		return obj.category.slug


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


@admin.register(ArticleBody)
class ArticleBodyAdmin(AdminBaseModel):
	def get_queryset(self, request):
		return super().get_queryset(request).select_related('article')

	list_display = [
		'get_article',
		'lang',
		'name',
	]
	fieldsets = (
		(None, {
			'fields': (
				('lang',), 
				'name',
				'short_desc',
				'content',
				'article',
			)
		}),
	)
	list_filter = (
		'article__is_valid', 
		'lang',
	)
	search_fields = ('article__slug',)
	ordering = ('-article__created_at',)
	raw_id_fields = ['article',]

	@admin.display(description='Article')
	def get_article(self, obj):
		return obj.article.slug