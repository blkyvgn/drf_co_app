from rest_framework import serializers
from api.vendors.helpers.translation import tr
from api.vendors.helpers.validators import (
	email_validation_check,
	passwd_validation_check,
)
from rest_framework.validators import UniqueValidator
from api.apps.account.models.account import Customer
from api.apps.account.models.account import Account


class AccountRegisterSerializer(serializers.ModelSerializer):
	email = serializers.EmailField(
		required=True,
		validators=[
			UniqueValidator(
				queryset=Account.objects.all(),
				message=tr('not_unique_user_email')
			)
		]
	)
	username = serializers.CharField(
		required=True,
		validators=[
			UniqueValidator(
				queryset=Account.objects.all(),
				message=tr('not_unique_username')
			)
		]
	)
	password = serializers.CharField(min_length=8, write_only=True)
	password_confirm = serializers.CharField(min_length=8, write_only=True)

	class Meta:
		model = Customer
		fields = (
			'email', 
			'username', 
			'password',
			'password_confirm',
		)
		extra_kwargs = {
			'password': {'write_only': True},
			'password_confirm': {'write_only': True},
		}

	def create(self, validated_data):
		password = validated_data.pop('password', None)
		del validated_data['password_confirm']
		instance = Account.objs.create(**validated_data)
		if password is not None:
			instance.set_password(password)
		instance.save()
		return instance

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

class MailSerializer(serializers.Serializer):
	email = serializers.EmailField()

	def validate_email(self, value):
		if not email_validation_check(value):
			raise serializers.ValidationError('Not valid email')
		return value

class NewPasswdSerializer(serializers.Serializer):
	password = serializers.CharField(max_length=50, required=False)
	password_confirm = serializers.CharField(max_length=50, required=False)

	def validate_password(self, value):
		if not passwd_validation_check(value):
			raise serializers.ValidationError('Not valid password')
		return value

	def validate(self, data):
		if data.get('password') is not None and data['password'] != data['password_confirm']:
			raise serializers.ValidationError('Passwords are not equal')
		return data

	def update(self, instance, validated_data):
		new_password = validated_data.get('password', instance.password)
		instance.set_password(new_password)
		instance.save()
		return instance

'''
{
"email":"u9@u.com",
"username":"user9",
"password":"12345678",
"password_confirm":"12345678"
}
'''