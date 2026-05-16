from django.db import models
from django.utils.text import slugify
from django.utils import timezone

class AnnouncementCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=120, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Announcement Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Announcement(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=270, blank=True)
    short_description = models.TextField(help_text="A brief summary for the card view.")
    full_description = models.TextField(blank=True, null=True, help_text="Detailed content of the announcement.")
    category = models.ForeignKey(AnnouncementCategory, on_delete=models.CASCADE, related_name='announcements')
    attachment = models.FileField(upload_to='announcements/attachments/', blank=True, null=True)
    publish_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publish_date', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
