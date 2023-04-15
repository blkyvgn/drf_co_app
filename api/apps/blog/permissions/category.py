from rest_framework import permissions



class ShowCategoryListPermission(permissions.BasePermission):
	
	def has_permission(self, request, view):
		return request.user.has_perm('blog.view_category')


class ShowCategoryPermission(permissions.BasePermission):
	
	def has_object_permission(self, request, view, obj):
		return request.user.has_perm('blog.view_category')


class CreateCategoryListPermission(permissions.BasePermission):
	
	def has_permission(self, request, view):
		return request.user.has_perm('blog.add_category')


class EditCategoryPermission(permissions.BasePermission):
	
	def has_object_permission(self, request, view, obj):
		return request.user.has_perm('blog.change_category')


class DeleteCategoryPermission(permissions.BasePermission):
	 
	def has_object_permission(self, request, view, obj):
		return request.user.has_perm('blog.delete_category')