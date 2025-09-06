from django.urls import path
from .views import PageSectionTraining, download_brochure

urlpatterns = [
    path('fetch-training-page/', PageSectionTraining.as_view(), name='page-section-list'),
    path('download_brochure/<int:pk>/', download_brochure, name='download-brochure'),
]
