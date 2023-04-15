from django.contrib import admin
from api.vendors.base.model import AdminBaseModel
from django.utils.translation import gettext_lazy as _
from api.apps.account.models import Contact


@admin.register(Contact)
class ContactAdmin(AdminBaseModel):
	model = Contact
	list_display = (
		'value',
		'default',
		'_type',
		'is_valid',
		'account',
	)
	list_filter = (
		'is_valid', 
		'_type',
	)
	fieldsets = (
		(None, {
			'fields': (
				'value',
				'default',
				'_type',
				'is_valid',
				'account',
			)
		}),
	)
	search_fields = ('account__email',)
	ordering = []
	raw_id_fields = ['account', ]