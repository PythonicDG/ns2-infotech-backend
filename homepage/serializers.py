from rest_framework import serializers
from .models import (
    PageSection, HeroSection, OverviewSection, WhyChooseUsSection,
    OurServicesSection, PlacementSection, TestimonialSection,
    FaqSection, ContactUsSection, CtaSection, SectionContent
)
from core.models import SocialLink, Announcement, SiteStatistic
from core.serializers import AnnouncementSerializer, SiteStatisticSerializer


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
    """
    Flat serializer to match the old JSON structure exactly.
    Includes all possible fields for every section to avoid breaking the frontend.
    """
    content_items = SectionContentSerializer(many=True, read_only=True)
    section_type = serializers.SerializerMethodField()
    
    # Common fields that might be null on some children
    super_heading = serializers.SerializerMethodField()
    heading = serializers.SerializerMethodField()
    subheading = serializers.SerializerMethodField()
    overview_text = serializers.SerializerMethodField()
    background_image = serializers.SerializerMethodField()
    primary_image = serializers.SerializerMethodField()
    
    primary_button_text = serializers.SerializerMethodField()
    primary_button_url = serializers.SerializerMethodField()
    secondary_button_text = serializers.SerializerMethodField()
    secondary_button_url = serializers.SerializerMethodField()

    social_links = serializers.SerializerMethodField()
    announcements = serializers.SerializerMethodField()
    statistics = serializers.SerializerMethodField()

    class Meta:
        model = PageSection
        fields = (
            'id', 'section_type', 'label', 'order', 'is_active',
            'super_heading', 'heading', 'subheading', 'overview_text',
            'background_image', 'primary_image', 
            'primary_button_text', 'primary_button_url', 'secondary_button_text', 'secondary_button_url',
            'content_items', 'social_links', 'announcements', 'statistics'
        )

    def get_section_type(self, obj):
        mapping = {
            'HeroSection': 'Hero Banner',
            'OverviewSection': 'Overview',
            'WhyChooseUsSection': 'Why Choose Us',
            'OurServicesSection': 'Our Services',
            'PlacementSection': 'KEY_ACHIVEMENTS',
            'TestimonialSection': 'Testimonials Slider',
            'FaqSection': 'Frequently Asked Questions',
            'ContactUsSection': 'Contact Us',
            'CtaSection': 'Call To Action',
        }
        return mapping.get(obj.__class__.__name__, obj.__class__.__name__.upper())

    # Helper to get field value regardless of which child it's on
    def _getattr(self, obj, attr):
        return getattr(obj, attr, None)

    def get_super_heading(self, obj): return self._getattr(obj, 'super_heading')
    def get_heading(self, obj): return self._getattr(obj, 'heading')
    def get_subheading(self, obj): return self._getattr(obj, 'subheading')
    def get_overview_text(self, obj): return self._getattr(obj, 'overview_text')
    
    def get_background_image(self, obj):
        img = self._getattr(obj, 'background_image')
        return self.context['request'].build_absolute_uri(img.url) if img else None

    def get_primary_image(self, obj):
        img = self._getattr(obj, 'primary_image')
        return self.context['request'].build_absolute_uri(img.url) if img else None

    def get_primary_button_text(self, obj): return self._getattr(obj, 'primary_button_text')
    def get_primary_button_url(self, obj): return self._getattr(obj, 'primary_button_url')
    def get_secondary_button_text(self, obj): return self._getattr(obj, 'secondary_button_text')
    def get_secondary_button_url(self, obj): return self._getattr(obj, 'secondary_button_url')

    def get_social_links(self, obj):
        if isinstance(obj, ContactUsSection):
            links = SocialLink.objects.filter(is_active=True)
            return SocialLinkSerializer(links, many=True).data
        return None

    def get_announcements(self, obj):
        if isinstance(obj, HeroSection):
            items = Announcement.objects.filter(is_active=True).order_by('order')
            return AnnouncementSerializer(items, many=True).data
        return None

    def get_statistics(self, obj):
        if isinstance(obj, HeroSection):
            items = SiteStatistic.objects.filter(is_active=True).order_by('order')
            return SiteStatisticSerializer(items, many=True).data
        return None
