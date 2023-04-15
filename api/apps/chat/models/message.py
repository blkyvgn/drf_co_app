from django.db import models
from django.utils.translation import gettext_lazy as _
from api.vendors.base.model import BaseModel
from django.contrib.auth import get_user_model
from api.vendors.helpers.translation import tr
from api.vendors.mixins.model import TimestampsMixin

Account = get_user_model()


class Message(BaseModel, TimestampsMixin):
	message = models.CharField(
		max_length=255,
	)
	chat = models.ForeignKey(
		'Chat',
		verbose_name=_('Chat'), 
		on_delete=models.CASCADE
	)
	sender = models.ForeignKey(
		'account.Account', 
		verbose_name=_('Account'), 
		on_delete=models.CASCADE,
		related_name='messages_sent',
	)
	recipient = models.ForeignKey(
		'account.Account', 
		verbose_name=_('Account'), 
		on_delete=models.CASCADE,
		related_name='messages_received',
	)
	company = models.ForeignKey(
		'company.Company',
		on_delete=models.CASCADE, 
		related_name='messages',
	)

	class Meta:
		verbose_name = tr('message')
		verbose_name_plural = tr('messages')
		ordering = ('-created_at',)