from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnnouncementViewSet, AnnouncementCategoryViewSet

router = DefaultRouter()
router.register(r'items', AnnouncementViewSet, basename='announcement')
router.register(r'categories', AnnouncementCategoryViewSet, basename='announcement-category')

urlpatterns = [
    path('', include(router.urls)),
]
