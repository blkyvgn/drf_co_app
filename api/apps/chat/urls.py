from django.urls import path, include
from api.apps.chat.views import chat

app_name = 'chat'

urlpatterns = [
	path('room/<str:room_name>/', chat.RoomView.as_view(), name='room'),
]
