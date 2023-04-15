from django.conf import settings
from rest_framework import serializers
from api.apps.blog.models import Tag

class TagSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tag
		fields = [
			'tag', 
		]
		read_only_fields = ['id']