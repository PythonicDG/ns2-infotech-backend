# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import PageSection
# from .serializers import PageSectionSerializer
# import time
# import logging

# logger = logging.getLogger(__name__)

# class PortfolioSectionsAPIView(APIView):
#     def get(self, request, format=None):
#         start_time = time.time()
#         sections = PageSection.objects.filter(is_active=True) \
#             .prefetch_related('content_items') \
#             .order_by('order')
#         db_fetch_time = time.time()

#         serializer = PageSectionSerializer(sections, many=True)
#         serialize_time = time.time()

#         response = Response(serializer.data)
#         end_time = time.time()

#         logger.info(f"DB fetch time: {db_fetch_time - start_time:.3f}s")
#         logger.info(f"Serialization time: {serialize_time - db_fetch_time:.3f}s")
#         logger.info(f"Response build time: {end_time - serialize_time:.3f}s")
#         logger.info(f"Total API time: {end_time - start_time:.3f}s")

#         return response

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .pagination import PageSectionPagination
from .serializers import PageSectionSerializer
from .models import PageSection
from .serializers import PageSectionSerializer
import logging
import time

class PortfolioSectionsAPIView(APIView):
    pagination_class = PageSectionPagination()

    def get(self, request, format=None):
        queryset = PageSection.objects.filter(is_active=True).prefetch_related('content_items').order_by('order')

        paginator = self.pagination_class
        page = paginator.paginate_queryset(queryset, request, view=self)
        if page is not None:
            serializer = PageSectionSerializer(page, many=True)
            response = paginator.get_paginated_response(serializer.data)
        else:
            serializer = PageSectionSerializer(queryset, many=True)
            response = Response(serializer.data)

        return response
