from rest_framework import serializers
from .models import PageSection, SectionContent


class SectionContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionContent
        fields = [
            'id',
            'order',
            'is_active',
            'label',
            'title',
            'description',
            'text',
            'question',
            'answer',
            'primary_button_text',
            'primary_button_url',
            'secondary_button_text',
            'secondary_button_url',
            'image',
            'person_name',
            'person_role',
            'linkedin_url',
            'twitter_url',
            'facebook_url',
            'instagram_url',
        ]


class PageSectionSerializer(serializers.ModelSerializer):
    content_items = serializers.SerializerMethodField()

    def get_content_items(self, obj):
        return SectionContentSerializer(obj.content_items.filter(is_active=True).order_by('order'), many=True, context=self.context).data

    class Meta:
        model = PageSection
        fields = [
            'id',
            'section_type',
            'order',
            'is_active',
            'super_heading',
            'heading',
            'subheading',
            'overview_text',
            'background_image',
            'primary_image',
            'primary_button_text',
            'primary_button_url',
            'secondary_button_text',
            'secondary_button_url',
            'content_items',
        ]
