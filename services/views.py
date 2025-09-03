from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PageSection
from .serializers import PageSectionSerializer
from django.shortcuts import get_object_or_404
from core.models import SubMenu

class PageSectionListAPIView(APIView):
    def get(self, request):
        submenu_slug = request.query_params.get('submenu')
        section_type = request.query_params.get('section_type')
        is_active = request.query_params.get('is_active', 'true').lower() == 'true'

        queryset = PageSection.objects.prefetch_related('content_items').filter(is_active=is_active)

        if submenu_slug:
            submenu = get_object_or_404(SubMenu, slug = submenu_slug)
            queryset = queryset.filter(submenu = submenu)

        if section_type:
            queryset = queryset.filter(section_type = section_type)

        serializer = PageSectionSerializer(queryset.order_by('order'), many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
