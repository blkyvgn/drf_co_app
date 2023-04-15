from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.vendors.base.model import AdminBaseModel
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from api.apps.account.forms.admin.account import (
	AccountCreationForm, 
	AccountChangeForm,
)
from api.apps.account.models import (
	Account,
	Profile,
)

class ProfileInline(admin.StackedInline):
	model = Profile
	can_delete = False
	verbose_name_plural = _('Profile')
	fk_name = 'account'

@admin.register(Account)
class AccountAdmin(UserAdmin, AdminBaseModel):
	add_form = AccountCreationForm
	form = AccountChangeForm
	model = Account
	list_display = (
		'email', 
		'full_name',
		'is_valid',
		'is_staff', 
		'is_active', 
		'_type',
	)
	list_filter = (
		'is_valid',
		'is_staff', 
		'is_active', 
		'_type',
		'profile__sex',
	)
	fieldsets = (
		(None, {
			'fields': (
				'email', 
				'password',
			)
		}),
		('Permissions', {
			'fields': (
				'is_valid',
				'is_staff', 
				'is_active', 
				'_type', 
				'groups', 
				'user_permissions',
			)
		}),
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': (
				'email', 
				'password1', 
				'password2', 
				'is_valid',
				'is_staff', 
				'is_active', 
				'_type', 
				'groups', 
				'user_permissions',
			)}
		),
	)
	search_fields = ('email', 'profile__phone',)
	ordering = []

	@admin.display(description='Full name')
	def full_name(self, obj):
		return obj.profile.full_name

	list_select_related = [
		'profile', 
	]
	inlines = [
		ProfileInline, 
	]