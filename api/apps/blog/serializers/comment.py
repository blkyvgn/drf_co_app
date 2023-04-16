from django.conf import settings
from rest_framework import serializers
from api.vendors.base.serializer import BaseModelSerializer
from api.apps.company.models import Company
from api.apps.blog.models import Comment, Article

class CommentListSerializer(BaseModelSerializer):
	class Meta:
		model = Comment
		fields = [
			'username',
			'comment', 
		]
		read_only_fields = ['id']

class CommentSerializer(BaseModelSerializer):
	company_id = serializers.PrimaryKeyRelatedField(
		source='company',
		queryset=Company.objs.valid().all(),
		required=False,
	)
	article_id = serializers.PrimaryKeyRelatedField(
		source='article',
		queryset=Article.objs.valid().all(),
		required=False,
	)
	class Meta:
		model = Comment
		fields = [
			'username',
			'comment', 
			'article_id',
			'company_id'
		]
		read_only_fields = ['id']


	def create(self, validated_data):
		comment = Comment.objs.create(
			**validated_data,
			company_id=self.context.get('request').company.id, 
		)
		comment.save()
		return comment
'''
{
	"username":"user222",
	"comment":"some comment for article", 
	"article_id":1,
	"company_id":1
}
'''