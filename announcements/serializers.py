from rest_framework import serializers
from .models import Announcement, AnnouncementCategory

class AnnouncementCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementCategory
        fields = ['id', 'name', 'slug', 'is_active', 'created_at']

class AnnouncementSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    category_slug = serializers.ReadOnlyField(source='category.slug')

    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'slug', 'short_description', 'full_description',
            'category', 'category_name', 'category_slug', 'attachment',
            'publish_date', 'is_active', 'created_at', 'updated_at'
        ]
