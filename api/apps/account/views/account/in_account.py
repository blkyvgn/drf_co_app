from api.vendors.base.view import BaseAPIView, ProtectBaseAPIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from api.apps.account.serializers.account import (
	InAccountSerializer,
	InCreateUpdateAccountSerializer,
)
from api.apps.account.permissions.account import (
	ShowAccountListPermission,
	ShowAccountPermission,
	CreateAccountListPermission,
	EditAccountPermission,
	DeleteAccountPermission,
)
from django.http import (
	HttpResponse, 
	JsonResponse,
)
from rest_framework import status
from django.db.models import Count
Account = get_user_model()


class ListView(ProtectBaseAPIView):
	permission_classes = [ShowAccountListPermission]
	def get(self, request, format=None):
		accounts = Account.objs.select_related('profile').\
			annotate(articles_count=Count('articles')).\
			order_by('-created_at')
		accounts = InAccountSerializer.paginator(request, accounts)
		return Response({**accounts}, status=status.HTTP_200_OK)


class ItemView(ProtectBaseAPIView):
	permission_classes = [ShowAccountPermission]
	def get(self, request, pk, format=None):
		account = Account.objs.filter(id=int(pk)).\
			select_related('profile').\
			annotate(articles_count=Count('articles')).\
			first()
		if not account:
			return HttpResponse(status=status.HTTP_404_NOT_FOUND)
		serializer = InAccountSerializer(account)
		return Response(serializer.data)


class CreateView(ProtectBaseAPIView):
	permission_classes = [CreateAccountListPermission]
	def post(self, request, format=None):
		serializer = InCreateUpdateAccountSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response({'data':True}, status=status.HTTP_201_CREATED)


class EditView(ProtectBaseAPIView):
	permission_classes = [EditAccountPermission]
	def put(self, request, pk, format=None):
		account_id = int(pk)
		account = Account.objs.filter(id=account_id).first()
		if not account:
			return HttpResponse(status=status.HTTP_404_NOT_FOUND)
		serializer = InCreateUpdateAccountSerializer(data=request.data, instance=account)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response({'data':account_id}, status=status.HTTP_200_OK)


class DeleteView(ProtectBaseAPIView):
	permission_classes = [DeleteAccountPermission]
	def delete(self, request, pk, format=None):
		account = Account.objs.filter(id=int(pk)).first()
		if not account:
			return HttpResponse(status=status.HTTP_404_NOT_FOUND)
		account.profile.delete()
		account.delete()
		return Response({'success':'Deleted'}, status=status.HTTP_204_NO_CONTENT)

