from api.vendors.base.view import BaseAPIView, ProtectBaseAPIView
from api.vendors.helpers.request import get_filter_arguments
from django.utils.translation import get_language
from rest_framework.response import Response
from api.apps.video.models import Video
from api.apps.video.serializers.video import (
	VideoListSerializer,
	VideoSerializer,
)
from rest_framework import status
from django.http import Http404
from django.contrib.auth import get_user_model
Account = get_user_model()


class ListView(BaseAPIView):
	def get(self, request, format=None):
		videos = Video.objs.valid().company(request.company.id).\
			order_by('-created_at')
		videos = VideoListSerializer.paginator(request, videos)
		return Response({**videos}, status=status.HTTP_200_OK)


class ItemView(BaseAPIView):
	def get(self, request, pk, format=None):
		video = Video.objs.valid().company(request.company.id).\
			filter(pk=int(pk)).first()
		if not video:
			raise Http404('Video not found')
		serializer = VideoSerializer(video, context={'request':request})
		return Response(serializer.data, status=status.HTTP_200_OK)