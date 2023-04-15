from django.urls import path, include
from api.apps.company.front.views import (
	company as front,
	serv,
)

app_name = 'company'

urlpatterns = [
	path('out/', include([
		path('item/', front.CompanyView.as_view(), name='out_company'),
	])),
	path('translations/', serv.read_translations, name='translations'),
]
urlpatterns += [
	# path('in/', include([
	# 	path('item/', internal.show, name='in_company_item'),
	# ]))
]