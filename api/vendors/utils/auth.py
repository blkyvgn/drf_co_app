import logging
from django.contrib.auth.backends import ModelBackend
from rest_framework import authentication
from rest_framework import exceptions
from api.vendors.helpers.jwt import validate_request
from django.contrib.auth import get_user_model
Account = get_user_model()

logger = logging.getLogger('main')


class JwtAuthentication(authentication.BaseAuthentication):
	LOGIN_USER_MSG = 'LOGIN USER'
	LOGIN_USER_ERROR_MSG = 'LOGIN USER ERROR'
	INVALID_TOKEN = 'INVALID USER TOKEN'
	USER_NOT_EXIST_MSG = 'USER NOT EXIST OR NOT VALID'

	def authenticate(self, request):
		data = validate_request(request.headers)
		if not data:
			logger.info(f'{self.LOGIN_USER_MSG}-{self.INVALID_TOKEN}: {username}')
			return None, None
		try:
			user = Account.objs.get(id=data['account_id'])
			logger.info(f'{self.LOGIN_USER_MSG}: {username}')
		except Account.DoesNotExist:
			logger.info(
				f'{self.LOGIN_USER_ERROR_MSG}-{self.USER_NOT_EXIST_MSG}: {username}'
			)
			raise exceptions.AuthenticationFailed('No such account')

		return (user, None)