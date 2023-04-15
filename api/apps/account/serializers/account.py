from api.vendors.base.serializer import BaseModelSerializer, BaseSerializer
from rest_framework import serializers
from api.apps.account.models import (
	Account,
	Profile,
)
from api.vendors.helpers.validators import (
	email_validation_check,
	passwd_validation_check,
)


class InProfileSerializer(BaseModelSerializer):
	class Meta:
		model = Profile
		fields = [
			'full_name',
			'photo', 
			'phone', 
			'age', 
			'birthdate', 
			'sex',
		]

class InAccountSerializer(BaseModelSerializer):
	profile = InProfileSerializer()
	articles_count = serializers.SerializerMethodField()
	class Meta:
		model = Account
		fields = [
			'is_superuser',
			'username',
			'email',
			'is_staff',
			'is_active',
			'is_valid',
			'created_at',
			'updated_at',
			'articles_count',
			'profile',
		]

	def get_articles_count(self, obj):
		return obj.articles_count


# SEX_CHOICES = ['female', 'male']
SEX_CHOICES = Profile.Sex.choices

class InCreateUpdateAccountSerializer(BaseSerializer):
	email = serializers.EmailField()
	username = serializers.CharField(max_length=30)
	password = serializers.CharField(max_length=50, required=False)
	password_confirm = serializers.CharField(max_length=50, required=False)
	first_name = serializers.CharField(max_length=80)
	last_name = serializers.CharField(max_length=80)
	is_valid = serializers.BooleanField(default=False)
	sex = serializers.ChoiceField(choices=SEX_CHOICES, default='FEMALE')
	phone = serializers.CharField(max_length=80)
	age = serializers.IntegerField()

	def validate_age(self, value):
		if value < 1 or value > 120:
			raise serializers.ValidationError('Not valid age')
		return value

	def validate_email(self, value):
		if not email_validation_check(value):
			raise serializers.ValidationError('Not valid email')
		return value

	def validate_password(self, value):
		if not passwd_validation_check(value):
			raise serializers.ValidationError('Not valid password')
		return value

	def validate(self, data):
		if data.get('password') is not None and data['password'] != data['password_confirm']:
			raise serializers.ValidationError('Passwords are not equal')
		return data

	def create(self, validated_data):
		new_account = Account.objs.create(
			email = validated_data.get('email'),
			username = validated_data.get('username'),
			is_valid = validated_data.get('is_valid'),
		)
		new_account.set_password(validated_data.get('password'))
		new_account.save()
		new_profile = Profile.objects.create(
			account = new_account,
			first_name = validated_data.get('first_name'),
			last_name = validated_data.get('last_name'),
			sex = validated_data.get('sex'),
			phone = validated_data.get('phone'),
			age = validated_data.get('age'),
		)
		return new_account

	def update(self, instance, validated_data):
		instance.email = validated_data.get('email', instance.email)
		instance.username = validated_data.get('username', instance.username)
		instance.is_valid = validated_data.get('is_valid', instance.is_valid)
		if new_password := validated_data.get('password'):
			instance.set_password(new_password)
		instance.save()
		profile = instance.profile
		profile.first_name = validated_data.get('first_name', profile.first_name)
		profile.last_name = validated_data.get('last_name', profile.last_name)
		profile.sex = validated_data.get('sex', profile.sex)
		profile.phone = validated_data.get('phone', profile.phone)
		profile.age = validated_data.get('age', profile.age)
		profile.save()
		return instance


class OutAccountSerializer(BaseSerializer):
	first_name = serializers.CharField(max_length=80)
	middle_name = serializers.CharField(max_length=80)
	last_name = serializers.CharField(max_length=80)
	email = serializers.EmailField()
	username = serializers.CharField(max_length=30)
	sex = serializers.CharField(max_length=30)
	articles_count = serializers.IntegerField()
	articles_langs = serializers.CharField(max_length=30)

'''
{
"email":"u12@u.com",
"username":"user12",
"password":"12345678",
"password_confirm":"12345678",
"is_valid":"True",
"first_name":"user12",
"last_name":"User12",
"sex":"FEMALE",
"phone":"555-55-55-55",
"age":99
}
'''