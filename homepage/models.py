import io
import os
from PIL import Image as PilImage

from django.db import models
from django.core.files.base import ContentFile
from polymorphic.models import PolymorphicModel


class PageSection(PolymorphicModel):
    """
    Base model for all page sections. 
    Common fields like order and status live here.
    """
    label = models.CharField(
        max_length = 200, 
        blank = True, null = True, 
        help_text="Internal label (e.g. 'Main Hero' or 'Why Us Row 1'). Not shown on website."
    )
    order = models.PositiveIntegerField(
        default = 0,
        help_text="Control the sequence of sections on the page. Lower numbers appear first."
    )
    is_active = models.BooleanField(
        default = True,
        help_text="Uncheck this to hide the entire section from the website."
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.__class__.__name__}: {self.label or 'Unnamed Section'}"


class HeroSection(PageSection):
    super_heading = models.CharField(
        max_length=200, blank=True, null=True,
        help_text="Small 'eyebrow' text above the main banner title."
    )
    heading = models.CharField(
        max_length=255,
        help_text="The big main headline for the banner."
    )
    subheading = models.TextField(
        blank=True, null=True,
        help_text="Small description text below the main headline."
    )
    overview_text = models.CharField(
        max_length=255, blank=True, null=True,
        help_text="Extra text for additional details or small labels."
    )
    background_image = models.ImageField(
        upload_to='sections/hero/', blank=True, null=True,
        help_text="The large full-width image behind the text."
    )
    
    primary_button_text = models.CharField(max_length=50, blank=True, null=True)
    primary_button_url = models.CharField(max_length=200, blank=True, null=True)
    secondary_button_text = models.CharField(max_length=50, blank=True, null=True)
    secondary_button_url = models.CharField(max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        process_image(self.background_image)
        super().save(*args, **kwargs)


class OverviewSection(PageSection):
    heading = models.CharField(
        max_length=255,
        help_text="Heading for the Overview/About section."
    )
    subheading = models.TextField(
        blank=True, null=True,
        help_text="Detailed description or 'About' text."
    )
    primary_image = models.ImageField(
        upload_to='sections/overview/', blank=True, null=True,
        help_text="The main image shown next to the text."
    )
    overview_text = models.CharField(
        max_length=100, blank=True, null=True, 
        help_text="Tag/Badge text displayed near the image (e.g. '20+ Years Exp')."
    )
    
    primary_button_text = models.CharField(max_length=50, blank=True, null=True)
    primary_button_url = models.CharField(max_length=200, blank=True, null=True)
    secondary_button_text = models.CharField(max_length=50, blank=True, null=True)
    secondary_button_url = models.CharField(max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        process_image(self.primary_image)
        super().save(*args, **kwargs)


class WhyChooseUsSection(PageSection):
    heading = models.CharField(max_length=255, help_text="Header for the 'Why Choose Us' grid.")
    subheading = models.TextField(blank=True, null=True, help_text="Intro text for the cards below.")


class OurServicesSection(PageSection):
    heading = models.CharField(max_length=255, help_text="Main title for the services grid.")
    subheading = models.TextField(blank=True, null=True, help_text="Brief intro text for services.")


class PlacementSection(PageSection):
    heading = models.CharField(max_length=255, help_text="Title for the placed students slider.")
    subheading = models.TextField(blank=True, null=True, help_text="Subtitle for placement success.")


class TestimonialSection(PageSection):
    heading = models.CharField(max_length=255, help_text="Main headline for student reviews.")
    subheading = models.TextField(blank=True, null=True, help_text="Secondary text for reviews.")


class FaqSection(PageSection):
    heading = models.CharField(max_length=255, help_text="Title for the FAQ accordion.")
    subheading = models.TextField(blank=True, null=True, help_text="Intro for the questions.")


class ContactUsSection(PageSection):
    heading = models.CharField(max_length=255)
    subheading = models.TextField(blank=True, null=True)


class CtaSection(PageSection):
    heading = models.CharField(max_length=255, help_text="High-impact title for the Call to Action.")
    subheading = models.TextField(blank=True, null=True, help_text="Persuasive sub-text for the CTA.")
    primary_button_text = models.CharField(max_length=50, blank=True, null=True)
    primary_button_url = models.CharField(max_length=200, blank=True, null=True)


class SectionContent(models.Model):
    """
    Items that belong to a section (e.g. FAQ items, Service items).
    """
    section = models.ForeignKey(PageSection, related_name='content_items', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0, help_text="Controls item position.")
    is_active = models.BooleanField(default=True)

    label = models.CharField(max_length=100, blank=True, null=True, help_text="Optional internal label.")
    title = models.CharField(max_length=200, blank=True, null=True, help_text="Main text for this item (e.g. Service Name).")
    description = models.TextField(blank=True, null=True, help_text="Body text for the item/card.")
    text = models.CharField(max_length=255, blank=True, null=True, help_text="Extra small text or caption.")
    
    # Specific to FAQs
    question = models.CharField(max_length=255, blank=True, null=True, help_text="The question (FAQ only).")
    answer = models.TextField(blank=True, null=True, help_text="The answer (FAQ only).")

    icon = models.ImageField(upload_to='icons/', blank=True, null=True, help_text="SVG/Icon image for this item.")

    class Meta:
        ordering = ['section', 'order']

    def __str__(self):
        return self.title or self.question or self.label or f"Item #{self.id}"

    def save(self, *args, **kwargs):
        process_image(self.icon)
        super().save(*args, **kwargs)


def process_image(image_field):
    """Helper to process and convert images to WEBP"""
    if image_field and hasattr(image_field, 'file'):
        if not image_field.name.lower().endswith('.webp'):
            try:
                image = PilImage.open(image_field.file)
                image_io = io.BytesIO()
                image.save(image_io, format='WEBP', quality=85)
                image_io.seek(0)
                
                file_name = os.path.splitext(os.path.basename(image_field.name))[0]
                new_file_name = f"{file_name}.webp"
                image_field.save(new_file_name, ContentFile(image_io.read()), save=False)
            except Exception:
                pass
