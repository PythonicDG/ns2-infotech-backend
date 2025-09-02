from django.urls import path
from .views import PageSectionListAPIView

urlpatterns = [
    path('fetch-services/', PageSectionListAPIView.as_view(), name = 'page-section-list'),
]
