from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Menu,
    FooterSection,
    FooterSubscription,
    CompanyProfile,
)
from .serializers import (
    MenuSerializer,
    FooterSectionSerializer,
    FooterSubscriptionSerializer,
    CompanyProfileSerializer,
)

from rest_framework.decorators import api_view
from rest_framework import status
from .models import ContactMessage


class HeaderFooterAPIView(APIView):
    def get(self, request, format=None):
        menus = Menu.objects.filter(is_active=True).order_by('order')
        sections = FooterSection.objects.filter(is_active=True).order_by('order')
        subscription = FooterSubscription.objects.filter(is_active=True).first()
        company = CompanyProfile.objects.filter(is_active=True).first()

        data = {
            "header": {
                "menu": MenuSerializer(menus, many=True).data,
            },
            "footer": {
                "sections": FooterSectionSerializer(sections, many=True).data,
                "subscription": (
                    FooterSubscriptionSerializer(subscription).data
                    if subscription
                    else {}
                ),
                "company": (
                    CompanyProfileSerializer(company).data
                    if company
                    else {}
                ),
            },
        }

        return Response(data)

@api_view(['POST'])
def contact_form_submit(request):
    data = request.data

    full_name = data.get('full_name')
    email = data.get('email_address')
    phone = data.get('phone_number')
    subject = data.get('subject')
    message = data.get('message')

    if not full_name or not email or not subject or not message:
        return Response({
            "error": "Full name, email, subject, and message are required."
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        contact = ContactMessage.objects.create(
            full_name=full_name,
            email_address=email,
            phone_number=phone,
            subject=subject,
            message=message
        )
        return Response({
            "message": "success"
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            "error": "Something went wrong.",
            "details": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
