from api.vendors.base.view import BaseAPIView, ProtectBaseAPIView
from rest_framework.response import Response
from api.apps.blog.models import Comment
from api.apps.blog.serializers.comment import (
	CommentSerializer,
)
from rest_framework import status
from django.http import Http404
from django.contrib.auth import get_user_model
Account = get_user_model()


class ListView(BaseAPIView):
	def get(self, request, article_pk, format=None):
		comments = Comment.objs.valid().company(request.company.id).\
			filter(article_id=article_pk).\
			order_by('-created_at')
		comments = CommentSerializer.paginator(request, comments)
		return Response({**comments}, status=status.HTTP_200_OK)


class CreateView(BaseAPIView):
	def post(self, request, format=None):
		serializer = CommentSerializer(data=request.data, context={'request': request})
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response({'data':True}, status=status.HTTP_201_CREATED)