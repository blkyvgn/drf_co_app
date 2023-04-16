from api.vendors.base.view import BaseAPIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django.http import Http404
from rest_framework.renderers import TemplateHTMLRenderer

class RoomView(BaseAPIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'chat/room.html'

	def get(self, request, room_name):
		queryset = []
		return Response({'queryset': queryset})