from django.urls import path, include
# from api.apps.company.front.views import (
# 	company as front,
# 	serv,
# )

app_name = 'blog'

urlpatterns = [
	path('out/', include([
		# path('item/', internal.show, name='in_company_item'),
	])),
]
urlpatterns += [
	path('in/', include([
		# path('item/', internal.show, name='in_company_item'),
	]))
]