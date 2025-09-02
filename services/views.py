from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PageSection
from .serializers import PageSectionSerializer


class PageSectionListAPIView(APIView):
    def get(self, request):
        submenu_id = request.query_params.get('submenu')
        section_type = request.query_params.get('section_type')
        is_active = request.query_params.get('is_active', 'true').lower() == 'true'

        queryset = PageSection.objects.prefetch_related('content_items').filter(is_active = is_active)

        if submenu_id:
            queryset = queryset.filter(submenu_id = submenu_id)

        if section_type:
            queryset = queryset.filter(section_type = section_type)

        serializer = PageSectionSerializer(queryset.order_by('order'), many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
