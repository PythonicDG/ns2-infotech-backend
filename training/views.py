from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PageSection
from .serializers import PageSectionSerializer

class PageSectionList(APIView):

    def get(self, request, *args, **kwargs):
        page_sections = PageSection.objects.all().order_by('order')
        serializer = PageSectionSerializer(page_sections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
