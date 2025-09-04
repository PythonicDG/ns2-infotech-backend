from rest_framework import serializers
from .models import (
    Menu,
    SubMenu,
    FooterSection,
    FooterItem,
    FooterSubscription,
    CompanyProfile
)


class SubMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubMenu
        fields = ('text', 'url', 'order', 'slug')


class MenuSerializer(serializers.ModelSerializer):
    submenus = SubMenuSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = ('text', 'url', 'is_button', 'order', 'submenus')


class FooterItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterItem
        fields = ('text', 'url', 'icon', 'order')


class FooterSectionSerializer(serializers.ModelSerializer):
    items = FooterItemSerializer(many=True, read_only=True)

    class Meta:
        model = FooterSection
        fields = ('title', 'order', 'items')


class FooterSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterSubscription
        fields = ('placeholder_text', 'button_text')


class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = (
            'name',
            'logo',
            'tagline',
            'email',
            'phone',
            'copyright_text',
            'credits_text',
        )
