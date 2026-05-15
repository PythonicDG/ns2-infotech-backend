from django.urls import path
from .views import PageSectionsAPIView, ModuleListAPIView, ModuleDetailAPIView

urlpatterns = [
    path('fetch-module-page/', PageSectionsAPIView.as_view(), name='page_sections_api'),
    path('modules/', ModuleListAPIView.as_view(), name='module_list_api'),
    path('modules/<slug:slug>/', ModuleDetailAPIView.as_view(), name='module_detail_api'),
]
