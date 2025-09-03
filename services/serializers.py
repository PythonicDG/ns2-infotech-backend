from rest_framework import serializers
from .models import PageSection, SectionContent


class SectionContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionContent
        fields = [
            'id',
            'icon',
            'title',
            'description',
            'label_1',
            'label_2',
            'tags',
            'order',
            'is_active',
        ]


class PageSectionSerializer(serializers.ModelSerializer):
    content_items = SectionContentSerializer(many = True, read_only = True)

    class Meta:
        model = PageSection
        fields = [
            'id',
            'section_type',
            'order',
            'is_active',
            'super_heading',
            'heading',
            'highlighted_heading_text',
            'subheading',
            'primary_image',
            'background_image',
            'primary_button_text',
            'primary_button_url',
            'secondary_button_text',
            'secondary_button_url',
            'content_items',
        ]
