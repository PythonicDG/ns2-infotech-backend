from rest_framework import serializers
from .models import Announcement, AnnouncementCategory
from .content import safe_announcement_html

class AnnouncementCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementCategory
        fields = ['id', 'name', 'slug', 'is_active', 'created_at']

class AnnouncementSerializer(serializers.ModelSerializer):
    full_description = serializers.SerializerMethodField()
    category_name = serializers.ReadOnlyField(source='category.name')
    category_slug = serializers.ReadOnlyField(source='category.slug')

    def get_full_description(self, obj):
        return safe_announcement_html(obj.full_description)

    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'slug', 'short_description', 'full_description',
            'category', 'category_name', 'category_slug', 'attachment', 'image',
            'publish_date', 'is_active', 'created_at', 'updated_at'
        ]
