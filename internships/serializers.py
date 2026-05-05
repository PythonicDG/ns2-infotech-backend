from rest_framework import serializers
from .models import Module, PageSection, SectionContent


class SectionContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionContent
        fields = [
            'id', 'order', 'is_active', 'icon', 'label', 'title', 'description',
            'brochures', 'tags', 'primary_button_text', 'primary_button_url',
            'question', 'answer',
        ]


class PageSectionSerializer(serializers.ModelSerializer):
    content_items = SectionContentSerializer(many=True, read_only=True)

    class Meta:
        model = PageSection
        fields = [
            'id', 'section_type', 'order', 'is_active',
            'super_heading', 'heading', 'highlighted_heading', 'subheading',
            'background_image', 'primary_image',
            'overlay_title', 'overlay_description',
            'primary_button_text', 'primary_button_url',
            'secondary_button_text', 'secondary_button_url',
            'content_items',
        ]


class ModuleListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for module listing pages."""
    class Meta:
        model = Module
        fields = ['id', 'title', 'tagline', 'slug', 'thumbnail', 'is_active', 'order']


class ModuleDetailSerializer(serializers.ModelSerializer):
    """Full serializer for module detail pages with all sections and content."""
    sections = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = ['id', 'title', 'tagline', 'slug', 'thumbnail', 'is_active', 'sections']

    def get_sections(self, obj):
        active_sections = obj.sections.filter(is_active=True).prefetch_related('content_items').order_by('order')
        return PageSectionSerializer(active_sections, many=True, context=self.context).data
