from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
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

    def test_partners_are_ordered_and_drafts_are_hidden(self):
        partners = self.make_section('PARTNERS')
        partners.heading = 'Collaborators: AES & ADS'
        partners.subheading = 'In Strategic Partnership: Industrial Automation Solutions & Training'
        partners.save()
        SectionContent.objects.create(section=partners, title='ADS', order=2)
        SectionContent.objects.create(section=partners, title='AES', order=0)
        SectionContent.objects.create(section=partners, title='Draft partner', is_active=False)
        mia = SectionContent.objects.create(
            section=partners, title='MIA', order=1,
            description='Automation training',
        )
        # A stored logo reference is enough to verify the public media URL.
        SectionContent.objects.filter(pk=mia.pk).update(icon='company/logo/mia.webp')

        response = self.client.get(reverse('page-sections'))
        strip = response.data[0]
        self.assertEqual(strip['section_type'], 'Trust / Partners Strip')
        self.assertEqual(strip['heading'], partners.heading)
        self.assertEqual(strip['subheading'], partners.subheading)
        self.assertEqual([item['title'] for item in strip['content_items']], ['AES', 'MIA', 'ADS'])
        self.assertEqual(strip['content_items'][1]['description'], 'Automation training')
        self.assertTrue(strip['content_items'][1]['icon'].endswith('/media/company/logo/mia.webp'))

        partners.is_active = False
        partners.save()
        self.assertEqual(self.client.get(reverse('page-sections')).data, [])

    def test_partner_initialization_preserves_admin_edits(self):
        call_command('seed_partners')
        strip = PageSection.objects.get(section_type='PARTNERS')
        self.assertEqual(list(strip.content_items.values_list('title', flat=True)), ['AES', 'MIA', 'ADS'])
        strip.heading = 'Our industry partners'
        strip.save()
        strip.content_items.filter(title='ADS').delete()

        call_command('seed_partners')

        strip.refresh_from_db()
        self.assertEqual(PageSection.objects.filter(section_type='PARTNERS').count(), 1)
        self.assertEqual(strip.heading, 'Our industry partners')
        self.assertEqual(strip.content_items.count(), 2)
