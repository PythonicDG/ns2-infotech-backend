from django.urls import path
from .views import HomepageSectionsAPIView

urlpatterns = [
    path('fetch-homepage/', HomepageSectionsAPIView.as_view(), name = 'page-sections'),
]
