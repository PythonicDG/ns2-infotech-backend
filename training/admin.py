from django.contrib import admin
from .models import PageSection, SectionContent


class SectionContentInline(admin.StackedInline):
    model = SectionContent
    extra = 1
    fields = ['order', 'is_active', 'icon', 'label', 'title', 'description', 'brochures', 'tags', 'primary_button_text', 'primary_button_url']


class PageSectionAdmin(admin.ModelAdmin):
    list_display = ['section_type','submenu', 'order', 'is_active', 'super_heading', 'heading', 'highlighted_heading']
    list_filter = ['is_active', 'section_type']
    search_fields = ['heading', 'subheading', 'super_heading']
    ordering = ['order']

    inlines = [SectionContentInline]

    fieldsets = (
        (None, {
            'fields': ('section_type', 'submenu', 'order', 'is_active', 'super_heading', 'heading', 'highlighted_heading', 'subheading')
        }),
        ('Images', {
            'fields': ('background_image', 'primary_image', 'overlay_title', 'overlay_description')
        }),
        ('Buttons', {
            'fields': ('primary_button_text', 'primary_button_url', 'secondary_button_text', 'secondary_button_url')
        })
    )


class SectionContentAdmin(admin.ModelAdmin):
    list_display = ['section', 'order', 'title', 'is_active', 'label', 'linkedin_url', 'twitter_url', 'other_social_url']
    list_filter = ['is_active', 'section']
    search_fields = ['title', 'description', 'tags']
    ordering = ['section', 'order']

    fieldsets = (
        (None, {
            'fields': (
                'section', 'order', 'is_active', 'label', 'title', 'description', 'tags',
                'primary_button_text', 'primary_button_url',
                'linkedin_url', 'twitter_url', 'other_social_url',  # <--- Add here
            )
        }),
        ('Icon', {
            'fields': ('icon',)
        }),
    )


admin.site.register(PageSection, PageSectionAdmin)
admin.site.register(SectionContent, SectionContentAdmin)
