from rest_framework import permissions


class ShowAccountListPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return request.user.has_perm('account.view_account')


class ShowAccountPermission(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return request.user.has_perm('account.view_account')


class CreateAccountListPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return request.user.has_perm('account.add_account')


class EditAccountPermission(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return request.user.has_perm('account.change_account')


class DeleteAccountPermission(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return request.user.has_perm('account.delete_account')