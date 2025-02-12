from django.contrib import admin
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from django.urls import re_path


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    
    path('api/', include('apps.accounts.urls')),
    path('api/', include('apps.tools.urls')),
    path('api/', include('apps.products.urls')),
]
