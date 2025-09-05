from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import PageSection
from .serializers import PageSectionSerializer

@api_view(['GET'])
def about_page_data(request):
    sections = PageSection.objects.filter(is_active=True).order_by('order')
    serializer = PageSectionSerializer(sections, many=True, context={'request': request})
    return Response(serializer.data)