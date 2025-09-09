from django.urls import path
from .views import PageSectionsAPIView

urlpatterns = [
    path('fetch-internship-page/', PageSectionsAPIView.as_view(), name='page_sections_api'),
]
