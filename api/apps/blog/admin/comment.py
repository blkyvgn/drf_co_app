from django.contrib import admin
from api.vendors.base.model import AdminBaseModel
from api.apps.blog.models import Comment


@admin.register(Comment)
class CommentAdmin(AdminBaseModel):
	def get_queryset(self, request):
		return super().get_queryset(request).select_related('article')

	fieldsets = (
		(None, {
			'fields': (
				('is_valid',), 
				'username',
				'comment',
				'article',
				'company',
			)
		}),
	)
	list_display = [
		'username',
		'comment',
		'get_article',
	]
	raw_id_fields = ['article',]

	@admin.display(description='Article')
	def get_article(self, obj):
		return obj.article.slug