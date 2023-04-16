from rest_framework import permissions



class ShowVideoListPermission(permissions.BasePermission):
	
	def has_permission(self, request, view):
		return request.user.has_perm('article.view_article')


class ShowVideoPermission(permissions.BasePermission):
	
	def has_object_permission(self, request, view, obj):
		return obj.created_by == request.user \
			and request.user.has_perm('article.view_article')


class CreateVideoListPermission(permissions.BasePermission):
	
	def has_permission(self, request, view):
		return request.user.has_perm('article.add_article')


class EditVideoPermission(permissions.BasePermission):
	
	def has_object_permission(self, request, view, obj):
		return obj.created_by == request.user \
			and request.user.has_perm('article.change_article')


class DeleteVideoPermission(permissions.BasePermission):
	
	def has_object_permission(self, request, view, obj):
		return obj.created_by == request.user \
			and request.user.has_perm('article.delete_article')