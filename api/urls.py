from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import (
    path, 
    include,
    re_path,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('su-admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/', include([
        path('account/', include('api.apps.account.urls', namespace='account')),
        path('company/', include('api.apps.company.urls', namespace='company')),
        path('blog/', include('api.apps.blog.urls', namespace='blog')),
        path('video/', include('api.apps.video.urls', namespace='video')),
    ])),
    path('chat/', include('api.apps.chat.urls', namespace='chat')),

    re_path(r'^i18n/', include('django.conf.urls.i18n')),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ]