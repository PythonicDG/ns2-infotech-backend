from django.contrib import admin
from django.urls import path, include, re_path
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from core.dashboard import page_copy

urlpatterns = [
    path('', lambda request: redirect('admin/')),

    path('admin/', admin.site.urls),
    path('api/dashboard/', include('core.dashboard_urls')),
    path('api/page-copy/<str:page>/', page_copy),

    path('api/core/', include('core.urls')),
    path('api/homepage/', include('homepage.urls')),
    path('api/modules/', include('modules.urls')),
    path('api/contact/', include('contact.urls')),
    path('api/aboutus/', include('aboutus.urls')),
    path('api/announcements/', include('announcements.urls')),
    path('api/services/', include('services.urls')),


]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
