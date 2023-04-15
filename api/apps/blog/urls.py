from django.urls import path, include
from api.apps.blog.views.article import (
	in_article,
	out_article,
)
from api.apps.blog.views.category import (
	in_category,
	out_category,
)

app_name = 'blog'

urlpatterns = [
	path('article/', include([
		path('out/', include([
			path('list/', out_article.ListView.as_view(), name='out_articles'),
			path('item/<int:pk>/', out_article.ItemView.as_view(), name='out_article'),
		])),
	])),
	path('category/', include([
		path('out/', include([
			path('list/', out_category.ListView.as_view(), name='out_categories'),
			path('item/<int:pk>/', out_category.ItemView.as_view(), name='out_category'),
		])),
	])),
]
urlpatterns += [
	path('article/', include([
		path('in/', include([
			path('list/', in_article.ListView.as_view(), name='in_articles'),
			path('item/<int:pk>/', in_article.ItemView.as_view(), name='in_article'),
			path('create/', in_article.CreateView.as_view(), name='in_article_create'),
			path('edit/<int:pk>/', in_article.EditView.as_view(), name='in_article_edit'),
			path('delete/<int:pk>/', in_article.DeleteView.as_view(), name='in_article_delete'),
		])),
	])),
	path('category/', include([
		path('in/', include([
			path('list/', in_category.ListView.as_view(), name='in_categories'),
			path('item/<int:pk>/', in_category.ItemView.as_view(), name='in_category'),
			path('create/', in_category.CreateView.as_view(), name='in_category_create'),
			path('edit/<int:pk>/', in_category.EditView.as_view(), name='in_category_edit'),
			path('delete/<int:pk>/', in_category.DeleteView.as_view(), name='in_category_delete'),
		])),
	])),
]