from django.urls import path
from .views import PageSectionTraining

urlpatterns = [
    path('fetch-training-page/', PageSectionTraining.as_view(), name='page-section-list'),
]
