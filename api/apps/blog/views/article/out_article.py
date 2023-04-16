from api.vendors.base.view import BaseAPIView, ProtectBaseAPIView
from api.vendors.helpers.request import get_filter_arguments
from django.utils.translation import get_language
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.db.models.functions import Concat
from api.vendors.helpers.orm import GroupConcat
from api.apps.blog.models import (
	Article,
	ArticleBody,
	Comment,
	Tag,
)
from api.apps.blog.serializers.article import (
	OutArticleListSerializer,
	OutArticleSerializer,
)
from django.db.models import (
	F, Q, Func,
	Count,
	Case, Value, When,
	Prefetch,
)
from django.contrib.auth import get_user_model
Account = get_user_model()


class ListView(BaseAPIView):
	def get(self, request, format=None):
		search_name = get_filter_arguments(request).get('name', None)
		search_tag = get_filter_arguments(request).get('tag', None)
		articles = Article.objs.valid().company(request.company.id).\
			select_related('category').\
			select_related('author').\
			prefetch_related(
				Prefetch('body', 
					queryset=ArticleBody.objects.filter(lang=get_language()), 
				)
			).\
			annotate(
				comments_count=Count('comments'),
				articles_langs= GroupConcat('body__lang', True),
			).\
			filter(body__lang='en').\
			filter_by_params(_or=True, 
				body__name__icontains=search_name
			).\
			filter_by_params(_or=True, 
				tags__tag__icontains=search_tag
			).\
			order_by('-created_at').\
			distinct()
		articles = OutArticleListSerializer.paginator(request, articles)
		return Response({**articles}, status=status.HTTP_200_OK)


class ItemView(BaseAPIView):
	def get(self, request, pk, format=None):
		article = Article.objs.valid().company(request.company.id).\
			filter(id=int(pk)).\
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
			).first()
			# prefetch_related(
			# 	Prefetch('comments', 
			# 		queryset=Comment.objs.valid(), 
			# 	)
			# ).\
		if not article:
			raise Http404('Account not found')
		serializer = OutArticleSerializer(article, context={'request':request})
		return Response(serializer.data, status=status.HTTP_200_OK)