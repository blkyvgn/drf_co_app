from rest_framework.decorators import api_view
from django.utils.translation import get_language
from api.vendors.helpers.translation import tr
from rest_framework.response import Response

@api_view(['GET'])
def read_translations(request):
	lang = request.query_params.get('lang', get_language())
	params = request.query_params.get('trs', None)
	translations = tr(key=params, lang=lang)
	return Response(translations)