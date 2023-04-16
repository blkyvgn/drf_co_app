from django.views.decorators.http import require_http_methods
from django.http import StreamingHttpResponse
from django.shortcuts import (
	render, 
	get_object_or_404
)
from api.apps.video.models import Video
from api.apps.video.utils.file import open_file


@require_http_methods(['GET', 'POST'])
def get_video(request, pk: int):
    file, status_code, content_length, content_range = open_file(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response