from rest_framework import permissions



class ShowArticleListPermission(permissions.BasePermission):
	
	def has_permission(self, request, view):
		return request.user.has_perm('article.view_article')


class ShowArticlePermission(permissions.BasePermission):
	
	def has_object_permission(self, request, view, obj):
		return obj.author == request.user or obj.created_by == request.user \
			and request.user.has_perm('article.view_article')


class CreateArticleListPermission(permissions.BasePermission):
	
	def has_permission(self, request, view):
		return request.user.has_perm('article.add_article')


class EditArticlePermission(permissions.BasePermission):
	
	def has_object_permission(self, request, view, obj):
		return obj.author == request.user or obj.created_by == request.user \
			and request.user.has_perm('article.change_article')


class DeleteArticlePermission(permissions.BasePermission):
	
	def has_object_permission(self, request, view, obj):
		return obj.author == request.user or obj.created_by == request.user \
			and request.user.has_perm('article.delete_article')