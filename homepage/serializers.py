from rest_framework import serializers
from .models import PageSection, SectionContent
from core.models import SocialLink

class SectionContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionContent
        fields = (
            'label', 'title', 'description', 'text',
            'question', 'answer', 'icon', 'order', 'is_active'
        )

class SocialLinkSerializer(serializers.ModelSerializer):
    icon = serializers.ImageField(source='social_icon', read_only=True)
    url = serializers.CharField(source='social_link')

    class Meta:
        model = SocialLink
        fields = ('platform', 'icon', 'url')

class PageSectionSerializer(serializers.ModelSerializer):
    content_items = SectionContentSerializer(many=True, read_only=True)
    section_type = serializers.CharField(source='get_section_type_display')
    social_links = serializers.SerializerMethodField()

    class Meta:
        model = PageSection
        fields = (
            'section_type', 'order', 'is_active',
            'super_heading', 'heading', 'subheading', 'overview_text',
            'background_image', 'primary_image',
            'primary_button_text', 'primary_button_url',
            'content_items', 'social_links'
        )

    def get_social_links(self, obj):
        if obj.section_type == 'CONTACT_US':
            links = SocialLink.objects.filter(is_active=True)
            return SocialLinkSerializer(links, many=True).data
        return None
