from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PageSection
from .serializers import PageSectionSerializer
import time
import logging

logger = logging.getLogger(__name__)

class PortfolioSectionsAPIView(APIView):
    def get(self, request, format=None):
        start_time = time.time()
        sections = PageSection.objects.filter(is_active=True) \
            .prefetch_related('content_items') \
            .order_by('order')
        db_fetch_time = time.time()

        serializer = PageSectionSerializer(sections, many=True)
        serialize_time = time.time()

        response = Response(serializer.data)
        end_time = time.time()

        print(f"DB fetch time: {db_fetch_time - start_time:.3f}s")
        print(f"Serialization time: {serialize_time - db_fetch_time:.3f}s")
        print(f"Response build time: {end_time - serialize_time:.3f}s")
        print(f"Total API time: {end_time - start_time:.3f}s")

        return response