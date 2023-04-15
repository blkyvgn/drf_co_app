from api.apps.company.mixins.data import CompanyDataMixin
# from api.apps.category.mixins.data import CategoriesDataMixin
from django.http import Http404
from django.conf import settings
	
class RequestDataMixin(CompanyDataMixin):

	def dispatch(self, request, *args, **kwargs):
		alias = request.GET.get('alias', settings.COMPANY_ALIAS)
		company = self.get_company(alias=alias)
		setattr(request, 'company', company)
		return super().dispatch(request, *args, **kwargs)