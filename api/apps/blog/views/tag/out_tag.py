from api.vendors.base.view import BaseAPIView, ProtectBaseAPIView
from rest_framework.response import Response
from api.apps.blog.models import Comment
from api.apps.blog.serializers.tag import (
	TagSerializer,
)
from django.db.models import Q
from rest_framework import status
from django.http import Http404
from django.contrib.auth import get_user_model
Account = get_user_model()


class ListView(BaseAPIView):
	''' by: article_id or category_id '''
	def get(self, request, by:str, pk:int, format=None):
		tags = Tag.objs.valid().company(request.company.id).\
			filter(Q(**{by: pk})).\
			order_by('-created_at')
		tags = TagSerializer.paginator(request, tags)
		return Response({**tags}, status=status.HTTP_200_OK)


class CreateView(BaseAPIView):
	def post(self, request, format=None):
		serializer = TagSerializer(data=request.data, context={'request': request})
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response({'data':True}, status=status.HTTP_201_CREATED)