from django.contrib import admin
from django.urls import path, include, re_path
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('', lambda request: redirect('admin/')),

    path('admin/', admin.site.urls),

    path('api/core/', include('core.urls')),
    path('api/homepage/', include('homepage.urls')),
    path('api/services/', include('services.urls')),
    path('api/internships/', include('internships.urls')),
    path('api/training/', include('training.urls')),
    path('api/portfolio/', include('portfolio.urls')),
    path('api/contact/', include('contact.urls')),
    path('api/aboutus/', include('aboutus.urls')),

]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
