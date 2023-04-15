from django.db import models
from django.utils.translation import gettext_lazy as _
from api.vendors.base.model import BaseModel
from django.contrib.auth import get_user_model
from api.vendors.helpers.translation import tr
from api.vendors.mixins.model import (
	TimestampsMixin,
)
Account = get_user_model()


class Contact(BaseModel, TimestampsMixin):
	class Type(models.TextChoices):
		PHONE      = 'PHONE',      _('Phone')
		EMAIL      = 'EMAIL',      _('Email')
		SOCIAL_NET = 'SOCIAL_NET', _('Social net')

	value = models.CharField(
		max_length=255,
	)
	default = models.BooleanField(
		default=False
	)
	_type = models.CharField(db_column='type',
		max_length=15,
		choices=Type.choices,
		default=Type.PHONE,
		verbose_name=(_('Type'))
	)
	account = models.ForeignKey(
		Account, 
		verbose_name=_('Account'), 
		on_delete=models.CASCADE
	)

	class Meta:
		verbose_name = _('Contact')
		verbose_name_plural = _('Contacts')
		ordering = ('-created_at',)

	@property
	def type(self):
		return self._type

	@type.setter
	def type(self, val):
		self._type = val
