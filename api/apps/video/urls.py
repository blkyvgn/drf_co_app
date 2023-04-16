from django.urls import path, include
from api.apps.video.views import (
	stream,
	test,
)
from api.apps.video.views.video import (
	in_video,
	out_video,
)

app_name = 'video'

from rest_framework import routers

urlpatterns = [
	path('test/item/<int:pk>/', test.ItemView.as_view(), name='item'),
	path('stream/<int:pk>/', stream.get_video, name='stream'),
	path('out/', include([
		path('list/', out_video.ListView.as_view(), name='out_videos'),
		path('item/<int:pk>/', out_video.ItemView.as_view(), name='out_video'),
	])),
]
# urlpatterns += [
# 	path('in/', include([
# 		path('list/', in_video.ListView.as_view(), name='in_videos'),
# 		path('item/<int:pk>/', in_video.ItemView.as_view(), name='in_video'),
# 		path('create/', in_video.CreateView.as_view(), name='in_video_create'),
# 		path('edit/<int:pk>/', in_video.EditView.as_view(), name='in_video_edit'),
# 		path('delete/<int:pk>/', in_video.DeleteView.as_view(), name='in_video_delete'),
# 	]))
# ]

router = routers.DefaultRouter()
router.register('in', in_video.VideoViewSet)

urlpatterns += router.urls