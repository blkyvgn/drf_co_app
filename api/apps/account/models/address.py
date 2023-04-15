from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from api.vendors.base.model import BaseModel
from django.contrib.auth import get_user_model
from api.vendors.helpers.translation import tr
from api.vendors.mixins.model import (
	TimestampsMixin,
)
Account = get_user_model()


class Address(BaseModel, TimestampsMixin):
	address_line = models.CharField(
		max_length=255,
	)
	address_line_2 = models.CharField(
		max_length=255,
		null=True,
		blank=True,
	)
	town_city = models.CharField(
		_('Town/City'), 
		max_length=150,
	)
	state = models.CharField(
		max_length=50,
		null=True,
		blank=True,
	)
	country = models.CharField(
		max_length=8, 
		choices=settings.COUNTRIES, 
		default=settings.COUNTRIES[0]
	)
	phone = models.CharField(
		max_length=50,
		null=True,
		blank=True,
	)
	postcode = models.CharField(
		max_length=50,
	)
	delivery_instructions = models.CharField(
		_('Delivery Instructions'), 
		max_length=255,
		null=True,
		blank=True,
	)
	is_default = models.BooleanField(
		default=False
	)
	account = models.ForeignKey(
		Account, 
		verbose_name=_('Account'), 
		on_delete=models.CASCADE,
		related_name='addresses',
	)

	class Meta:
		verbose_name = _('Address')
		verbose_name_plural = _('Addresses')
		ordering = ('-created_at',)
