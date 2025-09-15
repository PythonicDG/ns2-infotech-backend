from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PageSection, SectionContent
from .serializers import PageSectionSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view

class PageSectionTraining(APIView):

    def get(self, request, *args, **kwargs):
        slug = request.query_params.get('slug')

        if slug:
            page_sections = PageSection.objects.filter(submenu__slug=slug, is_active=True)
        else:
            page_sections = PageSection.objects.filter(is_active=True)

        page_sections = page_sections.order_by('order', 'order_level')

        serializer = PageSectionSerializer(page_sections, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

# @api_view(['GET'])
# def download_brochure(request, pk):
#     content_item = get_object_or_404(SectionContent, pk=pk)
#     brochure_file = content_item.brochures

#     if not brochure_file:
#         return Response({"detail": "Brochure file not found."}, status=status.HTTP_404_NOT_FOUND)

#     file_url = request.build_absolute_uri(brochure_file.url)
#     return Response({"brochure_url": file_url}, status=status.HTTP_200_OK)

@api_view(['GET'])
def download_brochure(request, pk):
    content_item = get_object_or_404(SectionContent, pk=pk)
    brochure_file = content_item.brochures

    if not brochure_file:
        return Response({"detail": "Brochure file not found."}, status=status.HTTP_404_NOT_FOUND)

    file_path = brochure_file.path
    if not os.path.exists(file_path):
        return Response({"detail": "File does not exist."}, status=status.HTTP_404_NOT_FOUND)

    response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
    response['Access-Control-Allow-Origin'] = 'https://nsinfotech.networkindia.com'
    response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'Origin, Content-Type, Accept, Authorization'
    return response