from django.urls import path
from .views import PageSectionsAPIView

urlpatterns = [
    path('fetch-homepage/', PageSectionsAPIView.as_view(), name = 'page-sections'),
]
