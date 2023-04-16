from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from api.vendors.base.serializer import (
	BaseModelSerializer, 
	BaseSerializer
)
from api.apps.company.models import Company
from api.apps.blog.models import (
	Category,
	Article,
	ArticleBody,
	Comment,
	Tag,
)
import json
from django.contrib.auth import get_user_model
Account = get_user_model()

class CommentListSerializer(BaseModelSerializer):
	class Meta:
		model = Comment
		fields = [
			'username',
			'comment', 
		]
		read_only_fields = ['id']

class TagListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tag
		fields = [
			'tag', 
		]
		read_only_fields = ['id']

class OutCategorySerializer(BaseModelSerializer):
	class Meta:
		model = Category
		fields = [
			'id',
			'name', 
		]
		read_only_fields = ['id']

class OutAuthorSerializer(BaseModelSerializer):
	class Meta:
		model = Account
		fields = [
			'id',
			'username', 
		]
		read_only_fields = ['id']

class OutArticleBodySerializer(BaseModelSerializer):
	class Meta:
		model = ArticleBody
		fields = [
			'lang',
			'name', 
			'short_desc',
			'content',
		]

class OutArticleSerializer(BaseModelSerializer):
	category = OutCategorySerializer()
	author = OutAuthorSerializer()
	body = OutArticleBodySerializer(many=True)
	# thumb = serializers.ImageField(required=False)
	comments_count = serializers.IntegerField()
	thumb = serializers.SerializerMethodField()
	comments = CommentListSerializer(many=True)
	tags = TagListSerializer(many=True)
	class Meta:
		model = Article
		fields = [
			'id',
			'category',
			'author',
			'thumb',
			'comments_count',
			'body',
			'comments',
			'tags'
		]

	def get_thumb(self, obj):
		request = self.context.get('request')
		img_url = obj.img_url_or_default('thumb', settings.DEFAULT_IMAGE['PLACEHOLDER'])
		return f'{request.scheme}://{request.get_host()}{img_url}'


class OutArticleBodyListSerializer(BaseModelSerializer):
	class Meta:
		model = ArticleBody
		fields = [
			'lang',
			'name', 
			'short_desc',
		]

class OutArticleListSerializer(BaseSerializer):
	id = serializers.IntegerField(read_only=True)
	category = OutCategorySerializer()
	author = OutAuthorSerializer()
	body = OutArticleBodyListSerializer(many=True)
	comments_count = serializers.IntegerField()
	articles_langs = serializers.CharField()
	# thumb = serializers.ImageField(required=False)
	thumb = serializers.SerializerMethodField()

	class Meta:
		model = Article
		fields = [
			'id',
			'category',
			'author',
			'thumb',
			'body',
			'comments_count',
			'articles_langs',
		]

	def get_thumb(self, obj):
		request = self.context.get('request')
		img_url = obj.img_url_or_default('thumb', settings.DEFAULT_IMAGE['PLACEHOLDER'])
		return f'{request.scheme}://{request.get_host()}{img_url}'

# class OutArticleListSerializer(serializers.Serializer):
# 	id = serializers.IntegerField(read_only=True)
# 	cat = serializers.SerializerMethodField()
# 	owner = serializers.CharField()
# 	comments_count = serializers.IntegerField()
# 	langs = serializers.CharField()
# 	name = serializers.CharField()

# 	def get_cat(self, obj):
# 		return json.loads(obj.cat)


class InCategorySerializer(BaseModelSerializer):
	class Meta:
		model = Category
		fields = [
			'id',
			'name', 
		]
		read_only_fields = ['id']

class InAuthorSerializer(BaseModelSerializer):
	class Meta:
		model = Account
		fields = [
			'id',
			'username', 
		]
		read_only_fields = ['id']

class InArticleBodySerializer(BaseModelSerializer):
	class Meta:
		model = ArticleBody
		fields = [
			'lang',
			'name', 
			'short_desc',
			'content',
		]

class InArticleSerializer(BaseModelSerializer):
	category = InCategorySerializer()
	author = InAuthorSerializer()
	body = InArticleBodySerializer(many=True)
	thumb = serializers.ImageField(required=False)
	class Meta:
		model = Article
		fields = [
			'id',
			'category',
			'author',
			'body',
			'thumb',
		]

# class InArticleListSerializer(serializers.Serializer):
# 	id = serializers.IntegerField(read_only=True)
# 	cat = serializers.SerializerMethodField()
# 	owner = serializers.CharField()
# 	comments_count = serializers.IntegerField()
# 	langs = serializers.CharField()
# 	name = serializers.CharField()

# 	def get_cat(self, obj):
# 		return json.loads(obj.cat)

class InArticleListSerializer(BaseSerializer):
	id = serializers.IntegerField(read_only=True)
	category = InCategorySerializer()
	author = InAuthorSerializer()
	body = InArticleBodySerializer(many=True)
	comments_count = serializers.IntegerField()
	articles_langs = serializers.CharField()
	thumb = serializers.ImageField(required=False)

	class Meta:
		model = Article
		fields = [
			'id',
			'category',
			'author',
			'thumb',
			'body',
			'comments_count',
			'articles_langs',
		]

class InCreateUpdateArticleBodySerializer(BaseModelSerializer):
	class Meta:
		model = ArticleBody
		fields = [
			'lang',
			'name', 
			'short_desc',
			'content',
		]

class InCreateUpdateArticleSerializer(BaseModelSerializer):
	company_id = serializers.PrimaryKeyRelatedField(
		source='company',
		queryset=Company.objs.all(),
		required=False,
	)
	category_id = serializers.PrimaryKeyRelatedField(
		source='category',
		queryset=Category.objs.valid().all()
	)
	author_id = serializers.PrimaryKeyRelatedField(
		source='author',
		queryset=Account.objs.valid().all()
	)
	body = InCreateUpdateArticleBodySerializer(many=True)
	tags = TagListSerializer(many=True)
	class Meta:
		model = Article
		fields = [
			'slug',
			'category_id',
			'author_id',
			'thumb',
			'body',
			'company_id',
		]
		validators = [
			UniqueTogetherValidator(
				queryset=Article.objects.all(),
				fields=['slug', 'company_id']
			)
		]


	def validate_body(self, value):
		if not isinstance(value, list):
			serializers.ValidationError('body not a list')
		for item in value:
			serializer = InCreateUpdateArticleBodySerializer(data=item)
			serializer.is_valid(raise_exception=True)
		return value

	def create(self, validated_data):
		bodies = validated_data.pop('body')
		tags = validated_data.pop('tags')
		article = Article.objs.create(
			**validated_data, 
			created_by_id=self.context.get('request').user.id, 
			company_id=self.context.get('request').company.id 
		)
		for body in bodies:
			ArticleBody.objects.create(article=article, **body)
		article.save()
		tags_list = []
		for tag in tags:
			new_tag = Tag.objects.create(
				tag=tag, 
				article_id=article.id,
				company_id=self.context.get('request').company.id
			)
			tags_list.append(new_tag)
		if tags_list:
			article.tags.add(*tags_list)
		return article

	def update(self, instance, validated_data):
		bodies = validated_data.pop('body')
		tags = validated_data.pop('tags')
		instance.category = validated_data.get('category', instance.category)
		instance.author = validated_data.get('author', instance.author)
		instance.slug = validated_data.get('slug', instance.slug)
		updated_by_id = self.context.get('request').user.id 
		instance_body = list(instance.body.all())
		for body in bodies:
			inst_body = [ab for ab in instance_body if ab.lang == body['lang']][0]
			for field, value in body.items():
				setattr(inst_body, field, value)
			inst_body.save()
		instance.save()
		instance.tags.clear()
		tags_list = []
		for tag in tags:
			new_tag = Tag.objects.create(
				tag=tag, 
				article_id=instance.id,
				company_id=self.context.get('request').company.id
			)
			tags_list.append(new_tag)
		if tags_list:
			instance.tags.add(*tags_list)
		return instance
