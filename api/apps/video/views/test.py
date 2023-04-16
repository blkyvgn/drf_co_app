from api.vendors.base.view import BaseAPIView, BaseViewSet
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.renderers import TemplateHTMLRenderer
from api.apps.video.models import Video


class ItemView(BaseAPIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'video/stream.html'

	def get(self, request, pk):
		video = Video.objs.valid().filter(pk=pk).first()
		if video:
			return Response({'video': video})
		return Http404(status=status.HTTP_404_NOT_FOUND)
