from django.core.paginator import Paginator
from django.conf import settings

class SerializerHelpers:
	def get_img_url(self, request, img_url):
		return f'{request.scheme}://{request.get_host()}{img_url}'

	@classmethod
	def paginator(cls, request, queryset, number_per_page=settings.NUMBER_PER_PAGE):
		paginator = Paginator(queryset, number_per_page)
		page_number = request.GET.get('page')
		data = paginator.get_page(page_number)
		pages_data = {
			'previous_page': data.previous_page_number() if data.has_previous() else None,
			'next_page': data.next_page_number() if data.has_next() else None,
			'num_pages': data.paginator.num_pages,
		}
		serialize = cls(data, many=True, context={'request':request})

		return {**pages_data, 'data': serialize.data}