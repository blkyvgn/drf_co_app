from django.db import models
from django.utils.translation import gettext_lazy as _
from api.vendors.base.model import BaseModel
from django.contrib.auth import get_user_model
from api.vendors.helpers.translation import tr
from api.vendors.mixins.model import TimestampsMixin

Account = get_user_model()


class Chat(BaseModel, TimestampsMixin):
	slug = models.CharField(
		max_length=255,
	)
	account = models.ForeignKey(
		'account.Account', 
		verbose_name=_('Account'), 
		on_delete=models.CASCADE
	)
	company = models.ForeignKey(
		'company.Company',
		on_delete=models.CASCADE, 
		related_name='chats',
	)

	class Meta:
		verbose_name = tr('chat')
		verbose_name_plural = tr('chats')
		ordering = ('-created_at',)
		constraints = [
			models.UniqueConstraint(fields=['company_id', 'slug'], name='unique_chat_slug')
		]
		indexes = [
			models.Index(fields=('company_id', 'slug')),
		]