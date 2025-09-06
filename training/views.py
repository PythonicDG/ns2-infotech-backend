from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PageSection
from .serializers import PageSectionSerializer

class PageSectionTraining(APIView):

    def get(self, request, *args, **kwargs):
        slug = request.query_params.get('slug')  # e.g., ?slug=corporate-training

        if slug:
            page_sections = PageSection.objects.filter(submenu__slug=slug, is_active=True).order_by('order')
        else:
            page_sections = PageSection.objects.filter(is_active=True).order_by('order')

        serializer = PageSectionSerializer(page_sections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
