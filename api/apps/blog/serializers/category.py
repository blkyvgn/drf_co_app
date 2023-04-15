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
		img_url = obj.img_url_or_default('thumb', settings.DEFAULT_IMAGE['PLACEHOLDER'])
		return f'{request.scheme}://{request.get_host()}{img_url}'

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
		img_url = obj.img_url_or_default('thumb', settings.DEFAULT_IMAGE['PLACEHOLDER'])
		return f'{request.scheme}://{request.get_host()}{img_url}'


class InCreateCategorySerializer(BaseModelSerializer):
	company_id = serializers.PrimaryKeyRelatedField(
		source='company',
		queryset=Company.objs.all(),
	)
	cat_name = serializers.CharField()
	cat_short_desc = serializers.CharField()
	parent_id = serializers.PrimaryKeyRelatedField(
		source='parent',
		queryset=Category.objs.all(),
		required=False,
	)
	parent = InParentCategorySerializer(read_only=True)

	class Meta:
		model = Category
		fields = [
			'slug',
			'is_valid',
			'parent_id',
			'parent',
			'cat_name', 
			'cat_short_desc',
			'company_id'
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
		cat_name = validated_data.pop('cat_name')
		cat_short_desc = validated_data.pop('cat_short_desc')
		category = Category.objs.create(
			**validated_data,
			name=cat_name,
			short_desc=cat_short_desc,
			created_by_id=self.context.get('request').user.id, 
			company_id=self.context.get('request').company.id, 
		)
		category.save()
		return category
		

class InUpdateCategorySerializer(BaseModelSerializer):
	company_id = serializers.PrimaryKeyRelatedField(
		source='company',
		queryset=Company.objs.all(),
	)
	cat_name = serializers.CharField(required=False)
	cat_short_desc = serializers.CharField(required=False)
	parent_id = serializers.PrimaryKeyRelatedField(
		source='parent',
		queryset=Category.objs.all(),
		required=False,
	)
	parent = InParentCategorySerializer(read_only=True)
	class Meta:
		model = Category
		fields = [
			'slug',
			'is_valid',
			'parent_id',
			'parent',
			'company_id',
			'cat_name', 
			'cat_short_desc',
		]
		extra_kwargs = {'slug': {'required': False}} 
		validators = [
			UniqueTogetherValidator(
				queryset=Category.objects.all(),
				fields=['slug', 'company_id']
			)
		]

	def update(self, instance, validated_data):
		if cat_name := validated_data.get('cat_name'):
			instance.name = cat_name
		if cat_short_desc := validated_data.get('cat_short_desc'):
			instance.short_desc = cat_short_desc
		instance.slug = validated_data.get('slug', instance.slug)
		instance.is_valid = validated_data.get('is_valid', instance.is_valid)
		instance.parent = validated_data.get('parent', None)
		updated_by_id=self.context.get('request').user.id 
		instance.save()
		return instance


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
	class Meta:
		model = Category
		fields = [
			'id',
			'name', 
			'thumb',
			'short_desc',
			'articles_count',
			'parent',
			# 'children',
		]
		read_only_fields = ['id']

	def get_articles_count(self, obj):
		return obj.articles_count

	def get_thumb(self, obj):
		request = self.context.get('request')
		img_url = obj.img_url_or_default('thumb', settings.DEFAULT_IMAGE['PLACEHOLDER'])
		return f'{request.scheme}://{request.get_host()}{img_url}'
