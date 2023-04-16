from django.conf import settings
from rest_framework import serializers
from api.vendors.base.serializer import BaseModelSerializer
from django.core.validators import FileExtensionValidator
from api.apps.company.models import Company
from api.apps.video.models import Video

class VideoListSerializer(BaseModelSerializer):
	class Meta:
		model = Video
		fields = [
			'slug',
			'thumb',
			'file',
			'alt',
			'links',
		]
		read_only_fields = ['id']

class VideoSerializer(BaseModelSerializer):
	thumb = serializers.ImageField(
		validators=[
			FileExtensionValidator(allowed_extensions=settings.IMAGE_EXTS)
		]
	)
	file = serializers.FileField(
		validators=[
			FileExtensionValidator(allowed_extensions=settings.VIDEO_FILE_EXTS)
		]
	)
	company_id = serializers.PrimaryKeyRelatedField(
		source='company',
		queryset=Company.objs.valid().all(),
		required=False,
	)
	class Meta:
		model = Video
		fields = [
			'slug',
			'thumb',
			'file',
			'alt',
			'links',
			'company_id',
		]
		read_only_fields = ['id']


	def create(self, validated_data):
		video = Video.objs.create(
			**validated_data,
			company_id=self.context.get('request').company.id, 
		)
		video.save()
		if thumb := validated_data.get('thumb', None):
			video.resize_img('thumb', settings.IMAGE_WIDTH['THUMBNAIL'])
		# print(serializer.validated_data.get('thumb'))
		# print(serializer.validated_data.get('file'))
		return video

	def update(self, instance, validated_data):
		instance.slug = validated_data.get('slug', instance.slug)
		instance.thumb = validated_data.get('thumb', instance.thumb)
		instance.file = validated_data.get('file', instance.file)
		instance.alt = validated_data.get('alt', instance.alt)
		instance.links = validated_data.get('links', instance.links)
		instance.save()

	# def validate_thumb(self, value):
	# 	# if value.get_extension not in settings.IMAGE_EXTS:
	# 	# 	raise serializers.ValidationError('Invalid image extension')
	# 	return value

	# def validate_file(self, value):
	# 	# if value.get_extension not in settings.VIDEO_FILE_EXTS:
	# 	# 	raise serializers.ValidationError('Invalid video extension')
	# 	return value
'''
{
	"slug":"video-one",
	"thumb":"company/1/video/thumb/filename.png",
	"file":"company/1/video/filename.mp4",
	"alt":{"en":"Alt text"}, 
	"links":{"youtube":{"link":"video link","is_valid":"true"}},
	"company_id":1
}
'''
