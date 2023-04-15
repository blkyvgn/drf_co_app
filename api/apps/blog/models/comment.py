from django.db import models
from api.vendors.base.model import BaseModel
from api.vendors.mixins.model import TimestampsMixin
from api.vendors.helpers.translation import tr
from django.contrib.auth import get_user_model
Account = get_user_model()


class Comment(BaseModel, TimestampsMixin):
	username = models.CharField(
		max_length=180, 
		null=True, 
		blank=True,
	)
	comment = models.TextField(
		null=True, 
		blank=True,
	)
	article = models.ForeignKey(
		'Article', 
		on_delete=models.CASCADE, 
		related_name='comments',
	)
	company = models.ForeignKey(
		'company.Company',
		on_delete=models.CASCADE, 
		related_name='comp_comments',
	)

	class Meta:
		verbose_name = tr('comment')
		verbose_name_plural = tr('comments')