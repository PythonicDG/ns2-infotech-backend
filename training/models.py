import io
import os
from PIL import Image as PilImage
from django.db import models
from django.core.files.base import ContentFile
from core.models import SubMenu

class PageSection(models.Model):
    submenu = models.ForeignKey(SubMenu, related_name='training_sections', on_delete=models.CASCADE, null=True, blank=True)
    SECTION_TYPES = [
        ('HERO_CORPORATE', 'Hero Banner (Corporate)'),
        ('ABOUT_CORPORATE', 'About Section (Corporate)'),
        ('TRAINING_OFFERINGS', 'Training Offerings Section (Corporate)'),
        ('WHY_CHOOSE_US', 'Why Choose Us Section (Corporate)'),
        ('INDUSTRIES_SERVED', 'Industries Served Section (Corporate)'),
        ('TRAINING_PROCESS', 'Training Process Section (Corporate)'),
        ('HERO_STUDENT', 'Hero Banner (Student)'),
        ('TRAINING_OFFERINGS', 'Training Offerings Section (Student)'),
        ('HIGHLIGHTS', 'Highlights (Student)'),
        ('PROGRAM_STRUCTURE', 'Program Structure (Student)'),
        ('WHAT_YOU_WILL_LEARN', 'What You Will Learn (Student)'),
        ('UPCOMING_BATCHES', 'Upcoming Batches (Student)'),
        ('OUR_TRAINERS', 'Our Trainers Section'),
        ('FAQ', 'Frequently Asked Questions'),
    ]

    section_type = models.CharField(max_length = 50, choices = SECTION_TYPES)
    order = models.PositiveIntegerField(default = 0)
    is_active = models.BooleanField(default = True)

    super_heading = models.CharField(max_length = 200, blank = True, null = True, help_text = "e.g., 'About Our'")
    heading = models.CharField(max_length = 255, blank = True, null = True, help_text = "The main heading of the section.")
    highlighted_heading = models.CharField(max_length = 255, blank = True, null = True, help_text = "The part of the heading to be highlighted.")
    subheading = models.TextField(blank = True, null = True)

    background_image = models.ImageField(upload_to = 'sections/', blank = True, null = True)
    primary_image = models.ImageField(upload_to = 'sections/', blank = True, null = True, help_text = "e.g., the photo in the 'About' section")

    overlay_title = models.CharField(max_length = 200, blank = True, null = True)
    overlay_description = models.TextField(blank = True, null = True)

    primary_button_text = models.CharField(max_length = 50, blank = True, null = True)
    primary_button_url = models.CharField(max_length = 200, blank = True, null = True)
    secondary_button_text = models.CharField(max_length = 50, blank = True, null = True)
    secondary_button_url = models.CharField(max_length = 200, blank = True, null = True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.get_section_type_display()}"

    def save(self, *args, **kwargs):
        def convert_to_webp(image_field):
            if image_field and hasattr(image_field, 'file'):
                image = PilImage.open(image_field.file)
                image_io = io.BytesIO()
                image.save(image_io, format = 'WEBP', quality = 85)
                image_io.seek(0)
                file_name = os.path.splitext(os.path.basename(image_field.name))[0]
                new_file_name = f"{file_name}.webp"
                image_field.save(new_file_name, ContentFile(image_io.read()), save = False)

        if self.background_image:
            convert_to_webp(self.background_image)
        if self.primary_image:
            convert_to_webp(self.primary_image)

        super().save(*args, **kwargs)


class SectionContent(models.Model):
    section = models.ForeignKey(PageSection, related_name = 'content_items', on_delete = models.CASCADE)
    order = models.PositiveIntegerField(default = 0)
    is_active = models.BooleanField(default = True)

    icon = models.ImageField(upload_to = 'icons/', blank = True, null = True)
    label = models.CharField(max_length = 100, blank = True, null = True, help_text = "e.g., the number '1' for a process step, or '500+' for a metric.")
    title = models.CharField(max_length = 200, blank = True, null = True, help_text = "The title of the card or item.")
    description = models.TextField(blank = True, null = True)
    brochures = models.FileField(upload_to='brochures/', blank=True, null=True)

    tags = models.CharField(max_length = 255, blank = True, null = True, help_text = "Comma-separated tags, e.g., Digital Skills,Data Analytics")

    primary_button_text = models.CharField(max_length = 50, blank = True, null = True)
    primary_button_url = models.CharField(max_length = 200, blank = True, null = True)

    linkedin_url = models.CharField(max_length = 200, blank = True, null = True)
    twitter_url = models.CharField(max_length = 200, blank = True, null = True)
    other_social_url = models.CharField(max_length = 200, blank = True, null = True, help_text = "For Dribbble, Medium, etc.")
    
    question = models.CharField(max_length = 500, blank = True, null = True, help_text = "Add Question for Faq")
    answer = models.CharField(max_length = 500, blank = True, null = True, help_text = "Add Answer for Faq")

    class Meta:
        ordering = ['section', 'order']

    def __str__(self):
        return self.title or f"Content Item for {self.section}"

    def save(self, *args, **kwargs):
        def convert_to_webp(image_field):
            if image_field and hasattr(image_field, 'file'):
                image = PilImage.open(image_field.file)
                image_io = io.BytesIO()
                image.save(image_io, format = 'WEBP', quality = 85)
                image_io.seek(0)
                file_name = os.path.splitext(os.path.basename(image_field.name))[0]
                new_file_name = f"{file_name}.webp"
                image_field.save(new_file_name, ContentFile(image_io.read()), save = False)

        if self.icon:
            convert_to_webp(self.icon)

        super().save(*args, **kwargs)
