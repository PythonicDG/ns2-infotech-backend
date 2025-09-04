from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
