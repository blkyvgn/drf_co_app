from django.conf import settings
from rest_framework import serializers
from api.vendors.base.serializer import BaseModelSerializer
from api.apps.blog.models import Comment


class CommentSerializer(BaseModelSerializer):
	class Meta:
		model = Comment
		fields = [
			'username',
			'comment', 
		]
		read_only_fields = ['id']