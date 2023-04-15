from django.conf import settings
from rest_framework import serializers
from api.vendors.base.serializer import BaseModelSerializer
from api.apps.company.models import Company

class OutCompanySerializer(BaseModelSerializer):
	articles_count = serializers.IntegerField()
	logo = serializers.SerializerMethodField()
	class Meta:
		model = Company
		fields = [
			'alias',
			'name',
			'logo',
			'options',
			'languages',
			'currencies',
			'articles_count',
		]
		read_only_fields = ['id']

	def get_logo(self, obj):
		request = self.context.get('request')
		logo_url = obj.img_url_or_default('logo', settings.DEFAULT_IMAGE['LOGO'])
		return self.get_img_url(request, logo_url)