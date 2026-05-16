from rest_framework import viewsets, filters
from .models import Announcement, AnnouncementCategory
from .serializers import AnnouncementSerializer, AnnouncementCategorySerializer

class AnnouncementCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AnnouncementCategory.objects.filter(is_active=True)
    serializer_class = AnnouncementCategorySerializer
    lookup_field = 'slug'

class AnnouncementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AnnouncementSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'short_description', 'full_description']
    ordering_fields = ['publish_date', 'created_at']
    ordering = ['-publish_date', '-created_at']

    def get_queryset(self):
        queryset = Announcement.objects.filter(is_active=True)
        category_slug = self.request.query_params.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset

