from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from api.vendors.base.model import BaseModel
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from api.vendors.helpers.translation import tr
from mptt.models import (
	MPTTModel, 
	TreeForeignKey, 
	TreeManyToManyField,
)
from api.vendors.mixins.model import (
	SoftdeleteMixin, 
	TimestampsMixin,
	ImgMixin,
	HelpersMixin,
	CacheMixin,
)
from api.vendors.helpers.model import (
	get_json_by_key,
	set_json_by_key,
)
Account = get_user_model()

def category_thumb_upload_to(instance, filename):
	return f'company/{instance.company}/categories/{instance.slug}/thumb/{filename}'


class Category(MPTTModel, BaseModel, TimestampsMixin, SoftdeleteMixin, HelpersMixin, ImgMixin, CacheMixin):
	CACHE_KEY = 'company-{0}-categories'

	slug = models.SlugField(
		max_length=150,
		help_text='format: required, letters, numbers, underscore, or hyphens'
	)
	_name = models.JSONField(db_column='name', 
		blank=True,
		default=dict
	)
	_short_desc = models.JSONField(db_column='short_desc', 
		blank=True,
		default=dict
	)
	thumb = models.ImageField(
		upload_to=category_thumb_upload_to, 
		null=True, 
		blank=True
	)
	parent = TreeForeignKey(
		'self',
		null=True,
		blank=True,
		on_delete=models.PROTECT,
		related_name='children',
		verbose_name=_('parent of category'),
		help_text=_('format: not required'),
	)
	position = models.IntegerField(
		default=0,
	)
	created_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='category_creator',
		null=True,
		blank=True,
	)
	updated_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='category_updater', 
		null=True,
		blank=True,
	)
	tags = models.ManyToManyField(
		'Tag',
		related_name='cat_tags',
	)
	company = models.ForeignKey(
		'company.Company',
		on_delete=models.CASCADE, 
		related_name='categories',
	)

	class MPTTMeta:
		order_insertion_by = ['slug']

	def __str__(self):
		return self.slug

	class Meta:
		verbose_name = tr('category')
		verbose_name_plural = tr('categories')
		constraints = [
			models.UniqueConstraint(fields=['company_id', 'slug'], name='unique_category_slug')
		]
		indexes = [
			models.Index(fields=('company_id', 'slug')), # condition='TRUE'
		]

	@property
	def name(self):
		return get_json_by_key(
			self._name, 
			key=get_language(), 
			default=settings.LANGUAGE_CODE
		)

	@name.setter
	def name(self, v):
		self._name = set_json_by_key(
			self._name, v, 
			key=get_language(), 
			default=settings.LANGUAGE_CODE
		)

	@property
	def short_desc(self):
		return get_json_by_key(
			self._short_desc, 
			key=get_language(), 
			default=settings.LANGUAGE_CODE
		)

	@short_desc.setter
	def short_desc(self, v):
		self._short_desc = set_json_by_key(
			self._short_desc, v, 
			key=get_language(), 
			default=settings.LANGUAGE_CODE
		)

	def save(self, *args, **kwargs):
		Category.delete_cache(self.company.alias)
		super().save(*args, **kwargs)
		self.resize_img('thumb', settings.IMAGE_WIDTH['THUMBNAIL'])
		# try:
		# 	with transaction.atomic():
		# 	Category.objects.rebuild() 
		# except DatabaseError:
		# 	pass

	def delete(self, *args, **kwargs):
		Category.delete_cache(self.company.alias)
		super().delete(*args, **kwargs)