from django.conf import settings
from rest_framework import serializers
from api.apps.company.models import Company
from api.apps.blog.models import Category, Article, Tag

class TagListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tag
		fields = [
			'tag', 
		]
		read_only_fields = ['id']

class TagSerializer(serializers.ModelSerializer):
	company_id = serializers.PrimaryKeyRelatedField(
		source='company',
		queryset=Company.objs.valid().all(),
		required=False,
	)
	category_id = serializers.PrimaryKeyRelatedField(
		source='article',
		queryset=Category.objs.valid().all(),
		required=False,
	)
	article_id = serializers.PrimaryKeyRelatedField(
		source='article',
		queryset=Article.objs.valid().all(),
		required=False,
	)
	class Meta:
		model = Tag
		fields = [
			'tag', 
			'article_id',
			'category_id',
			'company_id'
		]
		read_only_fields = ['id']

	def create(self, validated_data):
		tag = Tag.objs.create(
			**validated_data,
			company_id=self.context.get('request').company.id, 
		)
		tag.save()
		return comment

'''
{
	"tag":"user222",
	"article_id":1,
	"category_id":1,
	"company_id":1
}
'''