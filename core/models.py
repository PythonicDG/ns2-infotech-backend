import os
import io
from PIL import Image as PilImage
from django.core.files.base import ContentFile
from django.db import models
from django.utils.text import slugify


class Menu(models.Model):
    text = models.CharField(max_length = 100)
    url = models.CharField(max_length = 200, blank = True, null = True)
    is_button = models.BooleanField(default = False)
    order = models.PositiveIntegerField(default = 0)
    is_active = models.BooleanField(default = True)

    def __str__(self):
        return self.text


class SubMenu(models.Model):
    menu = models.ForeignKey(
        Menu, on_delete = models.CASCADE, related_name = 'submenus'
    )
    text = models.CharField(max_length = 100)
    url = models.CharField(max_length = 200)
    order = models.PositiveIntegerField(default = 0)
    is_active = models.BooleanField(default = True)
    slug = models.SlugField(unique = True, max_length = 50, null = True, blank = True)

    def __str__(self):
        return f"{self.menu.text} -> {self.text}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.text)
        super().save(*args, **kwargs)


class FooterSection(models.Model):
    title = models.CharField(max_length = 100)
    order = models.PositiveIntegerField(default = 0)
    is_active = models.BooleanField(default = True)

    def __str__(self):
        return self.title


class FooterItem(models.Model):
    section = models.ForeignKey(
        FooterSection, on_delete = models.CASCADE, related_name = 'items'
    )
    text = models.CharField(max_length = 200)
    url = models.CharField(max_length = 200, blank = True, null = True)
    icon = models.ImageField(
        upload_to = 'footer/icons/', blank = True, null = True
    )
    order = models.PositiveIntegerField(default = 0)
    is_active = models.BooleanField(default = True)

    def __str__(self):
        return f"{self.section.title} -> {self.text}"

    def save(self, *args, **kwargs):
        def save_image(image_field):
            if image_field and hasattr(image_field, 'path'):
                img = PilImage.open(image_field)
                img_io = io.BytesIO()
                img.save(img_io, format = 'WEBP')
                img_io.seek(0)

                filename = os.path.basename(image_field.name).rsplit('.', 1)[0] + '.webp'
                image_field.save(filename, ContentFile(img_io.read()), save = False)

        save_image(self.icon)
        super().save(*args, **kwargs)


class FooterSubscription(models.Model):
    placeholder_text = models.CharField(
        max_length = 100, default = "Enter your email"
    )
    button_text = models.CharField(max_length = 50, default = "Subscribe")
    is_active = models.BooleanField(default = True)

    def __str__(self):
        return f"Subscription Box - Active: {self.is_active}"


class CompanyProfile(models.Model):
    name = models.CharField(max_length = 200)
    tagline = models.CharField(max_length = 300, blank = True, null = True)
    description = models.TextField()
    logo = models.ImageField(
        upload_to = "company/logo/", blank = True, null = True
    )
    cover_image = models.ImageField(
        upload_to = "company/cover/", blank = True, null = True
    )
    email = models.EmailField(blank = True, null = True)
    phone = models.CharField(max_length = 20, blank = True, null = True)
    address = models.TextField(blank = True, null = True)
    is_active = models.BooleanField(default = True)
    copyright_text = models.CharField(
        max_length = 200, blank = True, null = True
    )
    credits_text = models.CharField(
        max_length = 200, blank = True, null = True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        def save_image(image_field):
            if image_field and hasattr(image_field, 'path'):
                img = PilImage.open(image_field)
                img_io = io.BytesIO()
                img.save(img_io, format = 'WEBP')
                img_io.seek(0)

                filename = os.path.basename(image_field.name).rsplit('.', 1)[0] + '.webp'
                image_field.save(filename, ContentFile(img_io.read()), save = False)

        save_image(self.logo)
        save_image(self.cover_image)
        super().save(*args, **kwargs)

class SocialLink(models.Model):
    platform = models.CharField(max_length=15)
    social_icon = models.ImageField(upload_to='slider/',max_length=255,null=True, blank=True)
    social_link = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.platform
    
    def save(self, *args, **kwargs):
        def save_image(image_field):
            if image_field:
                img = PilImage.open(image_field)
                img_io = io.BytesIO()
                img.save(img_io, format='WEBP')
                img_io.seek(0)
                current_path = image_field.path

                filename = os.path.basename(current_path).rsplit('.', 1)[0] +'.webp'

                image_field.save(filename, ContentFile(img_io.read()), save=False)

        save_image(self.social_icon)

        super().save(*args, **kwargs)

class ContactMessage(models.Model):
    SUBJECT_CHOICES = [
        ('general', 'General Inquiry'),
        ('project', 'Project Inquiry'),
        ('support', 'Support Request'),
        ('feedback', 'Feedback'),
    ]

    full_name = models.CharField(max_length=100)
    email_address = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.subject}"

class ContactInfo(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    working_hours = models.CharField(max_length=100)

    def __str__(self):
        return "Contact Information"