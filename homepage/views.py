from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PageSection
from .serializers import PageSectionSerializer


class PageSectionsAPIView(APIView):
    def get(self, request, format = None):
        sections = PageSection.objects.filter(is_active = True) \
            .select_related('content_type') \
            .prefetch_related('content_items') \
            .order_by('order')

        serializer = PageSectionSerializer(sections, many = True)
        return Response(serializer.data)
