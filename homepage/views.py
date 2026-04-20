from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PageSection
from .serializers import PageSectionSerializer


class HomepageSectionsAPIView(APIView):
    """
    API view to fetch all active homepage sections with their content items.
    """
    def get(self, request, format=None) -> Response:
        """
        Retrieves active page sections ordered by their sequence.
        """
        sections = PageSection.objects.filter(is_active=True) \
            .select_related('content_type') \
            .prefetch_related('content_items') \
            .order_by('order')

        serializer = PageSectionSerializer(sections, many=True)
        return Response(serializer.data)
