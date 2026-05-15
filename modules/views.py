from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Module, PageSection
from .serializers import PageSectionSerializer, ModuleListSerializer, ModuleDetailSerializer


class PageSectionsAPIView(APIView):
    """Fetch all active module page sections (standalone, no module)."""
    def get(self, request):
        sections = PageSection.objects.filter(
            is_active=True, module__isnull=True
        ).prefetch_related('content_items').order_by('order')
        
        serializer = PageSectionSerializer(sections, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ModuleListAPIView(APIView):
    """Fetch all active modules for listing pages."""
    def get(self, request):
        modules = Module.objects.filter(is_active=True).order_by('order')
        serializer = ModuleListSerializer(modules, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ModuleDetailAPIView(APIView):
    """Fetch a single module with all its sections and content items by slug."""
    def get(self, request, slug):
        module = get_object_or_404(Module, slug=slug, is_active=True)
        serializer = ModuleDetailSerializer(module, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
