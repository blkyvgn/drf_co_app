from api.vendors.base.view import BaseAPIView, ProtectBaseAPIView, BaseViewSet, ProtectBaseViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from api.apps.video.models import Video
from api.apps.video.serializers.video import (
	VideoListSerializer,
	VideoSerializer,
)
from api.apps.video.permissions.video import (
	ShowVideoListPermission,
	ShowVideoPermission,
	CreateVideoListPermission,
	EditVideoPermission,
	DeleteVideoPermission,
)
from rest_framework import status
from django.http import HttpResponse
from django.db.models import (
	F, 
	Count,
)
from rest_framework.decorators import action
from api.apps.blog.models import Category
from django.contrib.auth import get_user_model
Account = get_user_model()


class VideoViewSet(ProtectBaseViewSet):
	queryset = Video.objs.order_by('-created_at')
	serializer_class = VideoSerializer

	def list(self, request):
		videos = Video.objs.order_by('-created_at')
		videos = VideoListSerializer.paginator(request, videos)
		return Response({**videos}, status=status.HTTP_200_OK)

	def create(self, request):
		serializer = VideoSerializer(data=request.data, context={'request': request})
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response({'data':True}, status=status.HTTP_201_CREATED)

	def retrieve(self, request, pk=None):
		video = Video.objs.filter(id=int(pk)).first()
		if not video:
			return HttpResponse(status=status.HTTP_404_NOT_FOUND)
		serializer = VideoSerializer(video, context={'request':request})
		return Response(serializer.data, status=status.HTTP_200_OK)

	def update(self, request, pk=None):
		video_id = int(pk)
		video = Video.objs.filter(id=video_id).first()
		if not video:
			return HttpResponse(status=status.HTTP_404_NOT_FOUND)
		serializer = VideoSerializer(
			data=request.data, 
			instance=video, 
			context={'request': request}
		)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response({'data':video_id}, status=status.HTTP_200_OK)

	# def partial_update(self, request, pk=None):
	# 	pass

	def destroy(self, request, pk=None):
		video = Video.objs.filter(id=int(pk)).first()
		if not video:
			return HttpResponse(status=status.HTTP_404_NOT_FOUND)
		video.delete()
		return Response({'success':'Deleted'}, status=status.HTTP_204_NO_CONTENT)

	def get_permissions(self):
		if self.action == 'list':
			permission_classes = [ShowVideoListPermission]
		if self.action == 'create':
			permission_classes = [CreateVideoListPermission]
		if self.action == 'retrieve':
			permission_classes = [ShowVideoPermission]
		if self.action == 'update':
			permission_classes = [EditVideoPermission]
		if self.action == 'delete':
			permission_classes = [DeleteVideoPermission]
		else:
			permission_classes = [IsAuthenticated]
		return [permission() for permission in permission_classes]


# class ListView(ProtectBaseAPIView):
# 	permission_classes = [ShowVideoListPermission]
# 	def get(self, request, format=None):
# 		videos = Video.objs.order_by('-created_at')
# 		videos = VideoListSerializer.paginator(request, videos)
# 		return Response({**videos}, status=status.HTTP_200_OK)


# class ItemView(ProtectBaseAPIView):
# 	permission_classes = [ShowVideoPermission]
# 	def get(self, request, pk, format=None):
# 		video = Video.objs.filter(id=int(pk)).\
# 			first()
# 		if not video:
# 			return HttpResponse(status=status.HTTP_404_NOT_FOUND)
# 		serializer = VideoSerializer(video, context={'request':request})
# 		return Response(serializer.data, status=status.HTTP_200_OK)


# class CreateView(ProtectBaseAPIView):
# 	permission_classes = [CreateVideoListPermission]
# 	def post(self, request, format=None):
# 		serializer = VideoSerializer(data=request.data, context={'request': request})
# 		serializer.is_valid(raise_exception=True)
# 		serializer.save()
# 		return Response({'data':True}, status=status.HTTP_201_CREATED)


# class EditView(ProtectBaseAPIView):
# 	permission_classes = [EditVideoPermission]
# 	def put(self, request, pk, format=None):
# 		video_id = int(pk)
# 		video = Video.objs.filter(id=video_id).first()
# 		if not video:
# 			return HttpResponse(status=status.HTTP_404_NOT_FOUND)
# 		serializer = VideoSerializer(
# 			data=request.data, 
# 			instance=video, 
# 			context={'request': request}
# 		)
# 		serializer.is_valid(raise_exception=True)
# 		serializer.save()
# 		return Response({'data':video_id}, status=status.HTTP_200_OK)


# class DeleteView(ProtectBaseAPIView):
# 	permission_classes = [DeleteVideoPermission]
# 	def delete(self, request, pk, format=None):
# 		video = Video.objs.filter(id=int(pk)).first()
# 		if not video:
# 			return HttpResponse(status=status.HTTP_404_NOT_FOUND)
# 		video.delete()
# 		return Response({'success':'Deleted'}, status=status.HTTP_204_NO_CONTENT)

