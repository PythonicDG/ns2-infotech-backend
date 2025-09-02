import os
import io
from PIL import Image as PilImage
from django.core.files.base import ContentFile
from django.db import models


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

    def __str__(self):
        return f"{self.menu.text} -> {self.text}"


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
    facebook_url = models.URLField(blank = True, null = True)
    twitter_url = models.URLField(blank = True, null = True)
    linkedin_url = models.URLField(blank = True, null = True)
    instagram_url = models.URLField(blank = True, null = True)
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
