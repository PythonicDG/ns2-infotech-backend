from django.urls import path
from .views import PageSectionList

urlpatterns = [
    path('fetch-training-page/', PageSectionList.as_view(), name='page-section-list'),
]
