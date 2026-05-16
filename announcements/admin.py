from django.contrib import admin
from .models import Announcement, AnnouncementCategory

@admin.register(AnnouncementCategory)
class AnnouncementCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_filter = ('is_active',)

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'publish_date', 'is_active', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'short_description', 'full_description')
    list_filter = ('category', 'is_active', 'publish_date')
    ordering = ('-publish_date', '-created_at')
    date_hierarchy = 'publish_date'
    raw_id_fields = ('category',)
