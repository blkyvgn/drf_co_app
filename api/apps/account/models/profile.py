from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from api.vendors.base.model import EmptyBaseModel
from api.vendors.helpers.translation import tr
from api.vendors.mixins.model import (
	ImgMixin,
)
Account = get_user_model()

def profile_photo_upload_to(instance, filename):
	return f'account/{instance.id}/photo/{filename}'

class Profile(EmptyBaseModel, ImgMixin):
	class Sex(models.TextChoices):
		MALE    = 'MALE', _('Male')
		FEMALE  = 'FEMALE', _('Female')

	first_name = models.CharField(
		max_length=20, 
	)
	middle_name = models.CharField(
		max_length=20, 
		null=True, 
		blank=True,
	)
	last_name = models.CharField(
		max_length=20, 
	)
	photo = models.ImageField(
		upload_to=profile_photo_upload_to, 
		null=True, 
		blank=True,
	)
	phone = models.CharField(
		max_length=25, 
		null=True, 
		blank=True,
	)
	age = models.IntegerField(
		null=True, 
		blank=True,
	)
	birthdate = models.DateField(
		null=True, 
		blank=True,
	)
	sex = models.CharField(
		max_length=8, 
		choices=Sex.choices,
		default=Sex.MALE,
	)
	account = models.OneToOneField(
		Account, 
		on_delete=models.CASCADE,
		related_name='profile',
	)

	def __str__(self):
		return self.full_name

	@property
	def full_name(self):
		_middle_name = self.middle_name if self.middle_name else ''
		return f'{self.first_name} {_middle_name} {self.last_name}'

	@full_name.setter
	def full_name(self, val):
		first, *middle, last = val.split(' ')
		self.first_name = first
		self.middle_name = ' '.join(middle) if middle.len > 0 else None
		self.last_name = last

	class Meta:
		verbose_name = _('Profile')
		verbose_name_plural = _('Profiles')
