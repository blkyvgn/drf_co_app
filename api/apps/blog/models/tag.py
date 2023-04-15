from django.db import models
from api.vendors.base.model import BaseModel
from api.vendors.mixins.model import TimestampsMixin
from api.vendors.helpers.translation import tr
from django.contrib.auth import get_user_model
Account = get_user_model()


class Tag(BaseModel):
	tag = models.CharField(
		max_length=80, 
		null=True, 
		blank=True,
	)
	company = models.ForeignKey(
		'company.Company',
		on_delete=models.CASCADE, 
		related_name='comp_tags',
	)
	article = models.PositiveIntegerField()
	category = models.PositiveIntegerField() 

	class Meta:
		verbose_name = tr('tag')
		verbose_name_plural = tr('tags')