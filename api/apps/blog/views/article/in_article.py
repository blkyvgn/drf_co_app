from api.vendors.base.view import BaseAPIView, ProtectBaseAPIView
from api.vendors.helpers.request import get_filter_arguments
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from api.apps.blog.serializers.article import (	
	InArticleListSerializer,
	InArticleSerializer,
	InCreateUpdateArticleSerializer,
)
from django.http import HttpResponse
from django.db.models import (
	F, Q, Func,
	Count,
	Case, Value, When,
	Prefetch,
)
from django.db.models.functions import Concat
from api.vendors.helpers.orm import GroupConcat
from api.apps.blog.models import (
	Article,
	ArticleBody,
	Comment,
	Tag,
)
from api.apps.blog.permissions.article import (
	ShowArticleListPermission,
	ShowArticlePermission,
	CreateArticleListPermission,
	EditArticlePermission,
	DeleteArticlePermission,
)
import json
from django.contrib.auth import get_user_model
Account = get_user_model()


class ListView(ProtectBaseAPIView):
	permission_classes = [ShowArticleListPermission]
	def get(self, request, format=None):
		search_name = get_filter_arguments(request).get('name', None)
		# articles = Article.objs.by_raw(Article.raw_queries['out_list'], ['en'])
		articles = Article.objs.\
			select_related('category').\
			select_related('author').\
			prefetch_related(
				Prefetch('body', 
					queryset=ArticleBody.objects.filter(lang='en'), 
				)
			).\
			annotate(
				comments_count=Count('comments'),
				articles_langs= GroupConcat('body__lang', True),
			).\
			filter_by_params(_or=True, 
				body__name__icontains=search_name
			).\
			order_by('-created_at').\
			distinct()
		articles = InArticleListSerializer.paginator(request, articles)
		return Response({'articles': articles}, status=status.HTTP_200_OK)


class ItemView(ProtectBaseAPIView):
	permission_classes = [ShowArticlePermission]
	def get(self, request, pk, format=None):
		article = Article.objs.filter(id=int(pk)).\
			select_related('category').\
			select_related('author').\
			prefetch_related('body').\
			annotate(
				articles_count=Count('comments'),
				articles_langs= GroupConcat('body__lang', True),
			).first()
		if not article:
			raise Http404('Account not found')
		serializer = InArticleSerializer(article, context={'request':request})
		return Response(serializer.data, status=status.HTTP_200_OK)


class CreateView(ProtectBaseAPIView):
	permission_classes = [CreateArticleListPermission]
	def post(self, request, format=None):
		serializer = InCreateUpdateArticleSerializer(
			data=request.data, 
			context={'request': request}
		)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response({'data':True}, status=status.HTTP_201_CREATED)


# @parser_classes([MultiPartParser, FormParser])
class EditView(ProtectBaseAPIView):
	permission_classes = [EditArticlePermission]
	def put(self, request, pk, format=None):
		article_id = int(pk)
		article = Article.objs.filter(id=article_id).first()
		if not article:
			return Response(status=status.HTTP_404_NOT_FOUND)
		serializer = InCreateUpdateArticleSerializer(
			data=request.data, 
			instance=article, 
			context={'request': request}
		)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response({'data':article_id}, status=status.HTTP_200_OK)


class DeleteView(ProtectBaseAPIView):
	permission_classes = [DeleteArticlePermission]
	def delete(self, request, pk, format=None):
		article = Article.objs.filter(id=int(pk)).first()
		if not article:
			return HttpResponse(status=status.HTTP_404_NOT_FOUND)
		for body in article.body.all():
			body.delete()
		for comment in article.comments.all():
			comment.delete()
		article.delete()
		return Response({'success':'Deleted'}, status=status.HTTP_204_NO_CONTENT)

'''
{
    "slug":"qwerty", (unique)
    "category_id":1,
    "author_id":1,
    "company_id":1,
    "body": [
        {
            "lang":"en",
            "name":"ArticleEn",
            "short_desc":"Article short desc",
            "content":"Article body"
        },
        {
            "lang":"ru",
            "name":"ArticleRu",
            "short_desc":"Article short desc",
            "content":"Article body"
        }
    ]
}
'''