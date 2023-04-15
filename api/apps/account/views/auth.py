from api.vendors.base.view import BaseAPIView, ProtectBaseAPIView
from api.apps.company.tasks.mail import send_email_celery_task
from api.vendors.helpers.mail import get_activate_account_mail_body
from rest_framework_simplejwt.tokens import RefreshToken
from api.vendors.helpers.token import account_token
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.http import Http404
from api.apps.account.serializers.auth import (
	AccountRegisterSerializer,
	MailSerializer,
	NewPasswdSerializer,
)
Account = get_user_model()


class RegistrationView(BaseAPIView):
	def post(self, request, format=None):
		serializer = AccountRegisterSerializer(data=request.data)
		if serializer.is_valid():
			account = serializer.save()
			if account:
				account.send_registration_email(request)
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateView(BaseAPIView):
	def get(self, request, uid, token, format=None):
		user = Account.get_by_uid(uid)
		if user is not None and account_token.check_token(user, token):
			user.is_verified = True
			user.set_permissions()
			user.save(update_fields=['is_verified'])
		return Response({'msg':'account activated'}, status=status.HTTP_200_OK)


class LogoutView(BaseAPIView):
	def post(self, request, format=None):
		try:
			refresh_token = request.data['refresh_token']
			token = RefreshToken(refresh_token)
			token.blacklist()
			return Response(status=status.HTTP_205_RESET_CONTENT)
		except Exception as e:
			return Response(status=status.HTTP_400_BAD_REQUEST)


class ResetPasswdMailView(BaseAPIView):
	def post(self, request, format=None):
		serializer = MailSerializer(data=request.data)
		if serializer.is_valid():
			email = request.data['email']
			account = Account.objs.valid().filter(email=email).first()
			if account:
				account.send_reset_passwd_email(request)
				return Response(
					{'msg':'chack email', 'data':serializer.data}, 
					status=status.HTTP_200_OK
				)
			return Response(status=status.HTTP_404_NOT_FOUND)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConfirmNewPasswdView(BaseAPIView):
	def get(self, request, uid, token, format=None):
		user = Account.get_by_uid(uid)
		if user is not None and account_token.check_token(user, token):
			self.request.session['user_uid'] = uid
			return Response({'msg':'account is valid'}, status=status.HTTP_200_OK)
		return Response(status=status.HTTP_404_NOT_FOUND)

class NewPasswdView(BaseAPIView):
	def post(self, request, format=None):
		account = Account.get_by_uid(self.request.session['user_uid'])
		serializer = NewPasswdSerializer(data=request.data, instance=account)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response({'msg':'password changed'}, status=status.HTTP_200_OK)