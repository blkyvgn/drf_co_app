from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from api.vendors.utils.auth import JwtAuthentication
from rest_framework.permissions import IsAuthenticated
from api.vendors.mixins.view import RequestDataMixin
from rest_framework import viewsets


class BaseAPIView(RequestDataMixin, APIView):
	pass

class ProtectBaseAPIView(RequestDataMixin, APIView):
	authentication_classes = [
		SessionAuthentication, 
		JwtAuthentication,
	]
	permission_classes = [IsAuthenticated]


class BaseViewSet(RequestDataMixin, viewsets.ViewSet):
	pass 

class ProtectBaseViewSet(RequestDataMixin, viewsets.ViewSet):
	authentication_classes = [
		SessionAuthentication, 
		JwtAuthentication,
	]
	permission_classes = [IsAuthenticated]
