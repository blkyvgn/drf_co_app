from django.contrib import admin
from api.vendors.base.model import AdminBaseModel
from api.apps.blog.models import Tag


@admin.register(Tag)
class TagAdmin(AdminBaseModel):
	def get_queryset(self, request):
		return super().get_queryset(request)

	list_display = [
		'tag',
	]

	# @admin.display(description='Article')
	# def get_article(self, obj):
	# 	return obj.article.slug