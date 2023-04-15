from django.contrib import admin
from api.vendors.base.model import AdminBaseModel
from django.utils.translation import gettext_lazy as _
from api.apps.account.models import Address


@admin.register(Address)
class AddressAdmin(AdminBaseModel):
	model = Address
	list_display = (
		'address_line',
		'address_line_2',
		'town_city',
		'state',
		'country',
		'phone',
		'postcode',
		'is_default',
		'is_valid',
		'account',
	)
	list_filter = (
		'is_valid', 
		'is_default',
	)
	fieldsets = (
		(None, {
			'fields': (
				'address_line',
				'address_line_2',
				'town_city',
				'state',
				'country',
				'phone',
				'postcode',
				'delivery_instructions',
				'is_default',
				'is_valid',
				'account',
			)
		}),
	)
	search_fields = ('town_city', 'phone', 'account__email',)
	ordering = []
	raw_id_fields = ['account', ]