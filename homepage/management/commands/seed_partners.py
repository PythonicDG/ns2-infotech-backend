from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from core.models import CompanyProfile
from homepage.models import PageSection, SectionContent


class Command(BaseCommand):
    help = 'Initialize the homepage partners strip without overwriting admin edits.'

    @transaction.atomic
    def handle(self, *args, **options):
        if PageSection.objects.filter(section_type='PARTNERS').exists():
            self.stdout.write('Partners strip already exists; existing content was preserved.')
            return

        company = CompanyProfile.objects.filter(is_active=True).order_by('pk').first()
        if not company:
            raise CommandError('Create an active Company Profile in admin before initializing partners.')

        section = PageSection.objects.create(
            content_type=ContentType.objects.get_for_model(company),
            object_id=company.pk,
            section_type='PARTNERS',
            label='Homepage strategic partners',
            heading='Collaborators: AES & ADS',
            subheading='In Strategic Partnership: Industrial Automation Solutions & Training',
            order=2,
        )
        for order, name in enumerate(('AES', 'MIA', 'ADS')):
            SectionContent.objects.create(
                section=section,
                title=name,
                icon=company.logo.name if name == 'MIA' and company.logo else '',
                order=order,
            )
        self.stdout.write(self.style.SUCCESS(
            'Partners strip created. Upload AES and ADS logos under Homepage > Page sections > Trust / Partners Strip.'
        ))
