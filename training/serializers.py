from rest_framework import serializers
from .models import PageSection, SectionContent

class SectionContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionContent
        fields = ['id', 'order', 'is_active', 'icon', 'label', 'title', 'description', 'tags', 
        'primary_button_text', 'primary_button_url', 'linkedin_url','twitter_url','other_social_url',
        'question', 'answer' ]


class PageSectionSerializer(serializers.ModelSerializer):
    submenu_slug = serializers.SlugRelatedField(
        source='submenu',
        read_only=True,
        slug_field='slug'
    )
    content_items = SectionContentSerializer(many=True, read_only=True)

    class Meta:
        model = PageSection
        fields = [
            'id', 'submenu_slug', 'section_type', 'order', 'is_active',
            'super_heading', 'heading', 'highlighted_heading', 'subheading',
            'background_image', 'primary_image', 'overlay_title', 'overlay_description',
            'primary_button_text', 'primary_button_url', 'secondary_button_text',
            'secondary_button_url', 'content_items'
        ]
