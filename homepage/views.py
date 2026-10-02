from django.db.models import Prefetch
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PageSection, SectionContent
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
            .prefetch_related(Prefetch(
                'content_items',
                queryset=SectionContent.objects.filter(is_active=True).order_by('order'),
                to_attr='active_content_items',
            ), 'content_object') \
            .order_by('order')

        serializer = PageSectionSerializer(sections, many=True, context={'request': request})
        response = Response(serializer.data)
        response['Cache-Control'] = 'public, max-age=60, stale-while-revalidate=300'
        return response
