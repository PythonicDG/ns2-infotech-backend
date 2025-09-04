import io
import os
from PIL import Image as PilImage

from django.db import models
from django.core.files.base import ContentFile
from core.models import SubMenu


class PageSection(models.Model):
    SECTION_TYPES = [
        ('BANNER', 'Banner'),
        ('TECH_GRID_1', 'Technology Grid 1'),
        ('TECH_GRID_2', 'Technology Grid 2'),
        ('PROCESS_STEPS', 'Development Process'),
        ('WHAT_WE_PROVIDE', 'What We Provide'),
        ('WHY_CHOOSE_OUR_SERVICES', 'Why Choose Our Services'),
        ('GET_IN_TOUCH', 'Get In Touch'),
        ('CTA', 'Call To Action (Dark)'),
    ]

    submenu = models.ForeignKey(SubMenu, related_name='page_sections', on_delete=models.CASCADE)
    
    section_type = models.CharField(max_length=50, choices=SECTION_TYPES)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    super_heading = models.CharField(max_length=200, blank=True, null=True, help_text="For BANNER: The small text above the main heading, e.g., 'Premium Development Services'")
    heading = models.CharField(max_length=255, blank=True, null=True, help_text="The main title of the section.")
    highlighted_heading_text = models.CharField(max_length=100, blank=True, null=True, help_text="For BANNER: The part of the heading to be highlighted, e.g., 'Digital Vision'")
    subheading = models.TextField(blank=True, null=True, help_text="The descriptive text under the main heading.")

    primary_image = models.ImageField(upload_to='sections/', blank=True, null=True, help_text="For BANNER: The main image on the right.")
    background_image = models.ImageField(upload_to='sections/backgrounds/', blank=True, null=True, help_text="For CTA: The dark background image.")

    primary_button_text = models.CharField(max_length=50, blank=True, null=True)
    primary_button_url = models.CharField(max_length=200, blank=True, null=True)
    secondary_button_text = models.CharField(max_length=50, blank=True, null=True)
    secondary_button_url = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ['submenu', 'order']
        verbose_name = "Service Page Section"
        verbose_name_plural = "Page sections"

    def __str__(self):
        return f"{self.get_section_type_display()} for {self.submenu.text}"

    def save(self, *args, **kwargs):
        def convert_to_webp(image_field):
            if image_field and hasattr(image_field, 'file'):
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

        if self.pk is None:
            convert_to_webp(self.primary_image)
            convert_to_webp(self.background_image)
            
        super().save(*args, **kwargs)


class SectionContent(models.Model):
    CONTENT_CATEGORIES = [
        ('FLOATING_CARD', 'Floating Card'),
        ('STAT_BAR', 'Stat Bar Item'),
    ]

    section = models.ForeignKey(PageSection, related_name='content_items', on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CONTENT_CATEGORIES, default='STAT_BAR')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    icon = models.ImageField(upload_to='icons/', blank=True, null=True, help_text="Icon for Tech Item or Process Step.")
    title = models.CharField(max_length=200, blank=True, null=True, help_text="Main text/title, e.g., 'React.js', 'Discovery', '500+'")
    description = models.TextField(blank=True, null=True, help_text="Descriptive text for the item.")
    tags = models.CharField(max_length=255, blank=True, null=True, help_text="For TECH_ITEM: Comma-separated tags, e.g., 'SSR/SSG, API Routes, Performance'")
    label = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['section', 'order']
        verbose_name = "Section Content Item"
        verbose_name_plural = "Section Content"

    def __str__(self):
        return self.title or f"Item for {self.section}"
    
    def save(self, *args, **kwargs):
        def convert_to_webp(image_field):
            if image_field and hasattr(image_field, 'file'):
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

        if self.pk is None:
            convert_to_webp(self.icon)

        super().save(*args, **kwargs)