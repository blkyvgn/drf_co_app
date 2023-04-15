from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from api.vendors.base.model import BaseModel
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
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

def company_logo_upload_to(instance, filename):
	return f'company/{instance.alias}/logo/{filename}'

class Company(BaseModel, TimestampsMixin, HelpersMixin, ImgMixin, CacheMixin):
	CACHE_KEY = 'company-{0}'

	alias = models.SlugField(
		max_length=30, 
		unique=True,
	)
	_name = models.JSONField(db_column='name',
		default=dict,
		blank=True,
	)
	logo = models.ImageField(
		upload_to=company_logo_upload_to, 
		null=True, 
		blank=True
	)
	phone = models.CharField(
		max_length=30, 
		null=True, 
		blank=True,
	)
	email = models.CharField(
		max_length=120, 
		null=True, 
		blank=True,
	)
	options = models.JSONField(
		blank=True,
		default=dict
	)

	def __str__(self):
		return self.alias

	class Meta:
		verbose_name =  _('Company')
		verbose_name_plural =  _('Companies')
		ordering = ('-created_at',)
		indexes = [
			models.Index(fields=['alias',]),
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

	def save(self, *args, **kwargs):
		if self.pk:
			Company.delete_cache(self.alias)
		super().save(*args, **kwargs)
		self.resize_img('logo', settings.IMAGE_WIDTH['LOGO'])

	def delete(self, *args, **kwargs):
		Company.delete_cache(self.alias)
		super().delete(*args, **kwargs)

	@property
	def languages(self):
		languages = self.options.get('languages', {})
		return {k: v for k, v in settings.LANGUAGES if k in languages}

	@property
	def currencies(self):
		currencies = self.options.get('currencies', {})
		return {k: v for k, *v in settings.CURRENCIES if k in currencies}

	@classmethod
	def get_from_cache(cls, **kwargs):
		return cls.objs.valid().filter(alias=kwargs.get('cache_key')).first()

	# @classmethod
	# def get_cache_key(cls, **kwargs):
	# 	return f'company-{kwargs.get("cache_key")}'