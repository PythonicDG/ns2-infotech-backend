from django.contrib import admin
from .models import (
    Menu,
    SubMenu,
    FooterSection,
    FooterItem,
    FooterSubscription,
    CompanyProfile, SocialLink, ContactMessage, ContactInfo
)


class SubMenuInline(admin.TabularInline):
    model = SubMenu
    extra = 1
    fields = ('text', 'url', 'order', 'is_active')
    ordering = ('order',)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('text', 'url', 'is_button', 'order', 'is_active')
    list_filter = ('is_active', 'is_button')
    search_fields = ('text', 'url')
    ordering = ('order',)
    inlines = [SubMenuInline]


@admin.register(SubMenu)
class SubMenuAdmin(admin.ModelAdmin):
    list_display = ('menu', 'text', 'url', 'order', 'is_active')
    list_filter = ('is_active', 'menu')
    search_fields = ('text', 'url')
    ordering = ('menu', 'order')


class FooterItemInline(admin.TabularInline):
    model = FooterItem
    extra = 1
    fields = ('text', 'url', 'icon', 'order', 'is_active')
    ordering = ('order',)


@admin.register(FooterSection)
class FooterSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)
    ordering = ('order',)
    inlines = [FooterItemInline]


@admin.register(FooterItem)
class FooterItemAdmin(admin.ModelAdmin):
    list_display = ('section', 'text', 'url', 'icon', 'order', 'is_active')
    list_filter = ('is_active', 'section')
    search_fields = ('text', 'url', 'icon')
    ordering = ('section', 'order')


@admin.register(FooterSubscription)
class FooterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('placeholder_text', 'button_text', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('placeholder_text', 'button_text')


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'email', 'phone')

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'social_link', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('platform', 'social_link')
    readonly_fields = ('social_icon_preview',)

    def social_icon_preview(self, obj):
        if obj.social_icon:
            return f'<img src="{obj.social_icon.url}" width="40" height="40" />'
        return "(No Image)"
    social_icon_preview.allow_tags = True
    social_icon_preview.short_description = "Icon Preview"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email_address', 'subject', 'submitted_at')
    list_filter = ('subject', 'submitted_at')
    search_fields = ('full_name', 'email_address', 'message')
    readonly_fields = ('submitted_at',)


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'working_hours')
    search_fields = ('email', 'phone')