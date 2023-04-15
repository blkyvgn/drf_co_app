from api.vendors.base.view import BaseAPIView, ProtectBaseAPIView
from api.apps.account.serializers.account import OutAccountSerializer
from django.db.models.functions import Concat
from api.vendors.helpers.orm import GroupConcat
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.db.models import F, Count
from rest_framework import status
from django.http import Http404
Account = get_user_model()


class ListView(BaseAPIView):
	def get(self, request, format=None):
		accounts = Account.objs.valid().select_related('profile').\
			values(
				'id',
				'username', 
				'email', 
				first_name = F('profile__first_name'),
				middle_name = F('profile__middle_name'),
				last_name = F('profile__last_name'),
				sex=F('profile__sex'),
				articles_count=Count('articles'),
				articles_langs= GroupConcat('articles__body__lang', True),
			).\
			order_by('-created_at')
		accounts = OutAccountSerializer.paginator(request, accounts)
		return Response({**accounts}, status=status.HTTP_200_OK)


class ItemView(BaseAPIView):
	def get(self, request, pk, format=None):
		account = Account.objs.valid().filter(id=int(pk)).\
			values(
				'id', 
				'username', 
				'email', 
				first_name = F('profile__first_name'),
				middle_name = F('profile__middle_name'),
				last_name = F('profile__last_name'),
				sex=F('profile__sex'),
				articles_count=Count('articles'),
				articles_langs= GroupConcat('articles__body__lang', True),
			).first()
		if not account:
			raise Http404('Account not found')
		serializer = OutAccountSerializer(account)
		return Response(serializer.data, status=status.HTTP_200_OK)
