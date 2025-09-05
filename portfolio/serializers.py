from rest_framework import serializers
from .models import PageSection, SectionContent


class SectionContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionContent
        fields = (
            'label', 'title', 'description', 'text', 'primary_button_text', 'primary_button_url', 'secondary_button_text', 'secondary_button_url',
            'question', 'answer', 'icon', 'order', 'is_active'
        )


class PageSectionSerializer(serializers.ModelSerializer):
    content_items = SectionContentSerializer(many = True, read_only = True)
    section_type = serializers.CharField(source = 'get_section_type_display')

    class Meta:
        model = PageSection
        fields = (
            'section_type', 'order', 'is_active',
            'super_heading', 'heading', 'subheading', 'overview_text',
            'background_image', 'primary_image',
            'primary_button_text', 'primary_button_url',
            'content_items'
        )
