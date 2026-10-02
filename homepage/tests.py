from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework.test import APITestCase

from core.models import CompanyProfile
from .models import PageSection, SectionContent


class HomepageSectionsAPITests(APITestCase):
    def setUp(self):
        self.company = CompanyProfile.objects.create(
            name="Modern Institute of Automation",
            description="Automation training institute",
            is_active=True,
        )
        self.content_type = ContentType.objects.get_for_model(self.company)

    def make_section(self, section_type, active=True):
        return PageSection.objects.create(
            content_type=self.content_type,
            object_id=self.company.pk,
            section_type=section_type,
            heading=section_type,
            is_active=active,
        )

    def test_returns_only_active_sections_and_items(self):
        hero = self.make_section("HERO")
        self.make_section("FAQ", active=False)
        SectionContent.objects.create(section=hero, title="Visible", is_active=True)
        SectionContent.objects.create(section=hero, title="Draft", is_active=False)

        response = self.client.get(reverse("page-sections"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["section_type"], "Hero Banner")
        self.assertEqual(
            [item["title"] for item in response.data[0]["content_items"]],
            ["Visible"],
        )

    def test_response_has_short_public_cache_policy(self):
        self.make_section("OVERVIEW")

        response = self.client.get(reverse("page-sections"))

        self.assertEqual(
            response.headers["Cache-Control"],
            "public, max-age=60, stale-while-revalidate=300",
        )
