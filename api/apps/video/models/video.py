from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from api.vendors.base.model import BaseModel
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from api.vendors.helpers.translation import tr
from api.vendors.mixins.model import (
	TimestampsMixin,
	ImgMixin,
	HelpersMixin,
)
Account = get_user_model()

def video_upload_to(instance, filename):
	return f'company/{instance.company.id}/video/{filename}'

def thumb_upload_to(instance, filename):
	return f'company/{instance.company.id}/video/thumb/{filename}'


class Video(BaseModel, TimestampsMixin, HelpersMixin, ImgMixin):
	slug = models.SlugField(
		max_length=150,
	)
	thumb = models.ImageField(
		upload_to=thumb_upload_to,
		null=True, 
		blank=True,
		validators=[
			FileExtensionValidator(allowed_extensions=settings.IMAGE_EXTS)
		]
	)
	file = models.FileField(
		upload_to=video_upload_to,
		validators=[
			FileExtensionValidator(allowed_extensions=settings.VIDEO_FILE_EXTS)
		]
	)
	links = models.JSONField( #{'youtube':{'link':'<youtube_link>','is_active':true}},}
		default=dict,
		null=True, 
		blank=True,
	)
	alt = models.JSONField(
		max_length=80, 
		null=True, 
		blank=True,
	)
	created_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='video_creator',
		null=True,
		blank=True,
	)
	updated_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='video_updater', 
		null=True,
		blank=True,
	)
	company = models.ForeignKey(
		'company.Company',
		on_delete=models.CASCADE, 
		related_name='video',
		null=True, 
		blank=True,
	)

	class Meta:
		verbose_name = tr('video')
		verbose_name_plural = tr('videos')
		constraints = [
			models.UniqueConstraint(fields=['company_id', 'slug'], name='unique_video_slug')
		]
		indexes = [
			models.Index(fields=('company_id', 'slug')),
		]