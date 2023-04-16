from api.vendors.base.view import BaseAPIView, ProtectBaseAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from api.apps.blog.serializers.category import (
	InCategoryListSerializer,
	InCategorySerializer,
	InCreateCategorySerializer,
	InUpdateCategorySerializer,
	InChildCategorySerializer,
)
from api.apps.blog.permissions.category import (
	ShowCategoryListPermission,
	ShowCategoryPermission,
	CreateCategoryListPermission,
	EditCategoryPermission,
	DeleteCategoryPermission,
)
from rest_framework import status
from django.http import HttpResponse
from django.db.models import (
	F, 
	Count,
)
from api.apps.blog.models import Category
from django.contrib.auth import get_user_model
Account = get_user_model()



class ListView(ProtectBaseAPIView):
	permission_classes = [ShowCategoryListPermission]
	def get(self, request, format=None):
		categories = Category.objs.select_related('parent').\
			annotate(articles_count=Count('articles')).\
			order_by('-created_at')
		categories = InCategoryListSerializer.paginator(request, categories)
		return Response({**categories}, status=status.HTTP_200_OK)


class ItemView(ProtectBaseAPIView):
	permission_classes = [ShowCategoryPermission]
	def get(self, request, pk, format=None):
		category = Category.objs.filter(id=int(pk)).\
			select_related('parent').\
			annotate(articles_count=Count('articles')).\
			first()
		if not category:
			return HttpResponse(status=status.HTTP_404_NOT_FOUND)
		serializer = InCategorySerializer(category, context={'request':request})
		children = Category.objs.valid().filter(parent_id=category.id)
		childs = InChildCategorySerializer.paginator(request, children)
		return Response({'category':serializer.data, 'child':childs}, status=status.HTTP_200_OK)


class CreateView(ProtectBaseAPIView):
	permission_classes = [CreateCategoryListPermission]
	def post(self, request, format=None):
		serializer = InCreateCategorySerializer(data=request.data, context={'request': request})
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response({'data':True}, status=status.HTTP_201_CREATED)


class EditView(ProtectBaseAPIView):
	permission_classes = [EditCategoryPermission]
	def put(self, request, pk, format=None):
		category_id = int(pk)
		category = Category.objs.filter(id=category_id).first()
		if not category:
			return HttpResponse(status=status.HTTP_404_NOT_FOUND)
		serializer = InUpdateCategorySerializer(
			data=request.data, 
			instance=category, 
			context={'request': request}
		)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response({'data':category_id}, status=status.HTTP_200_OK)


class DeleteView(ProtectBaseAPIView):
	permission_classes = [DeleteCategoryPermission]
	def delete(self, request, pk, format=None):
		category = Category.objs.filter(id=int(pk)).first()
		if not category:
			return HttpResponse(status=status.HTTP_404_NOT_FOUND)
		for child in category.children.all():
			child.delete()
		category.delete()
		return Response({'success':'Deleted'}, status=status.HTTP_204_NO_CONTENT)


'''
{
"slug":"cat-slug", (unique)
"name":"Cat3",
"short_desc":"qwerty qwerty",
"is_valid":"True",
"parent_id":1,
"company_id":1
}
'''
