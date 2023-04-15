from django.urls import path, include
from api.apps.company.views.company import out_company
from api.apps.company.views import serv

app_name = 'company'

urlpatterns = [
	path('out/', include([
		path('item/', out_company.ItemView.as_view(), name='out_company'),
	])),
	path('translations/', serv.read_translations, name='translations'),
	path('change-language/<str:lang>', serv.change_language, name='change_language'),
	
]
urlpatterns += [
	# path('in/', include([
	# 	path('item/', internal.show, name='in_company_item'),
	# ]))
]