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
	Tag,
)

class TagListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tag
		fields = [
			'tag', 
		]
		read_only_fields = ['id']

class OutParentCategorySerializer(BaseModelSerializer):
	thumb = serializers.SerializerMethodField()
	class Meta:
		model = Category
		fields = [
			'id',
			'name', 
			'thumb',
			'short_desc',
		]
		read_only_fields = ['id']

	def get_thumb(self, obj):
		request = self.context.get('request')
		img_url = obj.img_url_or_default('thumb', settings.DEFAULT_IMAGE['PLACEHOLDER'])
		return f'{request.scheme}://{request.get_host()}{img_url}'


class OutChildCategorySerializer(BaseModelSerializer):
	thumb = serializers.SerializerMethodField()
	class Meta:
		model = Category
		fields = [
			'id',
			'name', 
			'thumb',
			'short_desc',
		]
		read_only_fields = ['id']

	def get_thumb(self, obj):
		request = self.context.get('request')
		img_url = obj.img_url_or_default('thumb', settings.DEFAULT_IMAGE['PLACEHOLDER'])
		return f'{request.scheme}://{request.get_host()}{img_url}'

class OutCategoryListSerializer(BaseModelSerializer):
	parent = OutParentCategorySerializer(required=False)
	articles_count = serializers.SerializerMethodField()
	thumb = serializers.SerializerMethodField()
	class Meta:
		model = Category
		fields = [
			'id',
			'name', 
			'thumb',
			'short_desc',
			'articles_count',
			'parent',
		]
		read_only_fields = ['id']

	def get_articles_count(self, obj):
		return obj.articles_count

	def get_thumb(self, obj):
		request = self.context.get('request')
		img_url = obj.img_url_or_default('thumb', settings.DEFAULT_IMAGE['PLACEHOLDER'])
		return f'{request.scheme}://{request.get_host()}{img_url}'

class OutCategorySerializer(BaseModelSerializer):
	parent = OutParentCategorySerializer(required=False)
	# children = OutChildCategorySerializer(many=True)
	articles_count = serializers.SerializerMethodField()
	thumb = serializers.SerializerMethodField()
	tags = TagListSerializer(many=True)
	class Meta:
		model = Category
		fields = [
			'id',
			'name', 
			'thumb',
			'short_desc',
			'articles_count',
			'parent',
			'tags'
			# 'children',
		]
		read_only_fields = ['id']

	def get_articles_count(self, obj):
		return obj.articles_count

	def get_thumb(self, obj):
		request = self.context.get('request')
		img_url = obj.img_url_or_default('thumb', settings.DEFAULT_IMAGE['PLACEHOLDER'])
		return f'{request.scheme}://{request.get_host()}{img_url}'

class InParentCategorySerializer(BaseModelSerializer):
	class Meta:
		model = Category
		fields = [
			'id',
			'name', 
			'short_desc',
		]
		read_only_fields = ['id']

class InChildCategorySerializer(BaseModelSerializer):
	thumb = serializers.SerializerMethodField()
	class Meta:
		model = Category
		fields = [
			'id',
			'name', 
			'thumb',
			'short_desc',
		]
		read_only_fields = ['id']

	def get_thumb(self, obj):
		request = self.context.get('request')
		img_url = obj.img_url_or_default('thumb', settings.DEFAULT_IMAGE['PLACEHOLDER'])
		return f'{request.scheme}://{request.get_host()}{img_url}'


class InCategoryListSerializer(BaseModelSerializer):
	parent = InParentCategorySerializer(required=False)
	articles_count = serializers.SerializerMethodField()
	thumb = serializers.SerializerMethodField()
	class Meta:
		model = Category
		fields = [
			'id',
			'name', 
			'thumb',
			'short_desc',
			'is_valid',
			'created_at',
			'articles_count',
			'parent',
		]
		read_only_fields = ['id']

	def get_articles_count(self, obj):
		return obj.articles_count

	def get_thumb(self, obj):
		request = self.context.get('request')
		thumb_url = obj.img_url_or_default('thumb', settings.DEFAULT_IMAGE['LOGO'])
		return self.get_img_url(request, thumb_url)

class InCategorySerializer(BaseModelSerializer):
	parent = InParentCategorySerializer(required=False)
	# children = InChildCategorySerializer(many=True)
	articles_count = serializers.SerializerMethodField()
	class Meta:
		model = Category
		fields = [
			'id',
			'name', 
			'short_desc',
			'is_valid',
			'created_at',
			'articles_count',
			'parent',
			# 'children',
		]
		read_only_fields = ['id']

	def get_articles_count(self, obj):
		return obj.articles_count

	def get_thumb(self, obj):
		request = self.context.get('request')
		thumb_url = obj.img_url_or_default('thumb', settings.DEFAULT_IMAGE['LOGO'])
		return self.get_img_url(request, thumb_url)



class InCreateCategorySerializer(BaseModelSerializer):
	company_id = serializers.PrimaryKeyRelatedField(
		source='company',
		queryset=Company.objs.all(),
	)
	name = serializers.CharField()
	short_desc = serializers.CharField()
	parent_id = serializers.PrimaryKeyRelatedField(
		source='parent',
		queryset=Category.objs.all(),
		required=False,
	)
	parent = InParentCategorySerializer(read_only=True)
	tags = TagListSerializer(many=True)
	class Meta:
		model = Category
		fields = [
			'slug',
			'is_valid',
			'parent_id',
			'parent',
			'name', 
			'short_desc',
			'company_id',
			'tags'
		]
		validators = [
			UniqueTogetherValidator(
				queryset=Category.objects.all(),
				fields=['slug', 'company_id']
			)
		]

	# def get_comp(self, obj):
	# 	print(self.context)
	# 	# return self.context.get('request').company.id
	# 	return '10'

	def create(self, validated_data):
		tags = validated_data.pop('tags')
		# name = validated_data.pop('name')
		# short_desc = validated_data.pop('short_desc')
		category = Category.objs.create(
			**validated_data,
			# name=name,
			# short_desc=short_desc,
			created_by_id=self.context.get('request').user.id, 
			company_id=self.context.get('request').company.id, 
		)
		category.save()
		tags_list = []
		for tag in tags:
			new_tag = Tag.objects.create(
				tag=tag, 
				category_id=category.id,
				company_id=self.context.get('request').company.id
			)
			tags_list.append(new_tag)
		if tags_list:
			category.tags.add(*tags_list)
		return category
		

class InUpdateCategorySerializer(BaseModelSerializer):
	company_id = serializers.PrimaryKeyRelatedField(
		source='company',
		queryset=Company.objs.all(),
	)
	name = serializers.CharField(required=False)
	short_desc = serializers.CharField(required=False)
	parent_id = serializers.PrimaryKeyRelatedField(
		source='parent',
		queryset=Category.objs.all(),
		required=False,
	)
	parent = InParentCategorySerializer(read_only=True)
	tags = TagListSerializer(many=True)
	class Meta:
		model = Category
		fields = [
			'slug',
			'is_valid',
			'parent_id',
			'parent',
			'name', 
			'short_desc',
			'company_id',
		]
		extra_kwargs = {'slug': {'required': False}} 
		validators = [
			UniqueTogetherValidator(
				queryset=Category.objects.all(),
				fields=['slug', 'company_id']
			)
		]

	def update(self, instance, validated_data):
		print(instance)
		instance.name = validated_data.get('name', instance.name)
		instance.short_desc = validated_data.get('short_desc', instance.short_desc)
		instance.slug = validated_data.get('slug', instance.slug)
		instance.is_valid = validated_data.get('is_valid', instance.is_valid)
		instance.parent = validated_data.get('parent', None)
		updated_by_id=self.context.get('request').user.id 
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



