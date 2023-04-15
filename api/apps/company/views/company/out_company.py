from api.vendors.base.view import BaseAPIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django.http import Http404
from api.apps.company.models import Company
from api.apps.company.serializers.company import OutCompanySerializer

class ItemView(BaseAPIView):

	def get(self, request, format=None):
		company = Company.objs.valid().filter(id=request.company.id).\
			annotate(articles_count=Count('articles')).\
			first()
		if not company:
			raise Http404('Company not found')
		serializer = OutCompanySerializer(company, context={'request':request})
		return Response(serializer.data, status=status.HTTP_200_OK)