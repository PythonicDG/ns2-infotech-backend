from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PageSection
from .serializers import PageSectionSerializer
import time
import logging

logger = logging.getLogger(__name__)

class PortfolioSectionsAPIView(APIView):
    def get(self, request, format=None):
        data = cache.get('portfolio_sections')
        if not data:
            sections = PageSection.objects.filter(is_active=True) \
                .prefetch_related('content_items') \
                .order_by('order')
            serializer = PageSectionSerializer(sections, many=True)
            data = serializer.data
            cache.set('portfolio_sections', data, 60 * 5)

        return Response(data)
