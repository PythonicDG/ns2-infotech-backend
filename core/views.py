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
