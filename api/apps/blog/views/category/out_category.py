from api.vendors.base.view import BaseAPIView, ProtectBaseAPIView
from api.vendors.helpers.request import get_filter_arguments
from rest_framework.response import Response
from django.db.models.functions import Concat
from api.vendors.helpers.orm import GroupConcat
from api.apps.blog.models import Category
from rest_framework import status
from django.http import Http404
from api.apps.blog.serializers.category import (
	OutCategorySerializer,
	OutCategoryListSerializer,
	OutChildCategorySerializer,
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
		search_tag = get_filter_arguments(request).get('tag', None)
		categories = Category.objs.valid().company(request.company.id).\
			select_related('parent').\
			annotate(articles_count=Count('articles')).\
			filter_by_params(_or=True, 
				tags__tag__icontains=search_tag
			).\
			order_by('-created_at')
		categories = OutCategoryListSerializer.paginator(request, categories)
		return Response({**categories}, status=status.HTTP_200_OK)


class ItemView(BaseAPIView):
	def get(self, request, pk, format=None):
		category = Category.objs.valid().filter(id=int(pk)).\
			select_related('parent').\
			annotate(
				articles_count=Count('articles'),
				child_count=Count('children'),
			).\
			first()
		if not category:
			raise Http404('Category not found')
		serializer = OutCategorySerializer(category, context={'request':request})
		children = Category.objs.valid().filter(parent_id=category.id)
		childs = OutChildCategorySerializer.paginator(request, children)
		return Response({'category':serializer.data, 'child':childs}, status=status.HTTP_200_OK)