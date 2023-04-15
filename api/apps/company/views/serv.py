from rest_framework.decorators import api_view
from django.utils.translation import get_language
from api.vendors.helpers.translation import tr
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def read_translations(request):
	lang = request.query_params.get('lang', get_language())
	params = request.query_params.get('trs', None)
	translations = tr(key=params, lang=lang)
	return Response(translations, status=status.HTTP_200_OK)


@api_view(['GET'])
def change_language(request, lang):
	if lang in settings.LANGUAGE_CODES:
		request.session['lang'] = lang
		return Response({'lang':lang}, status=status.HTTP_200_OK)
	return Response(status=status.HTTP_404_NOT_FOUND)