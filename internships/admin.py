from django.contrib import admin
from .models import PageSection, SectionContent

class SectionContentInline(admin.StackedInline):
    model = SectionContent
    extra = 1
    fields = (
        'order', 'is_active', 'icon', 'label', 'title', 'description', 
        'brochures', 'tags', 'primary_button_text', 'primary_button_url', 
        'question', 'answer'
    )
    show_change_link = True

@admin.register(PageSection)
class PageSectionAdmin(admin.ModelAdmin):
    list_display = ('section_type', 'heading', 'order', 'is_active')
    list_filter = ('section_type', 'is_active')
    search_fields = ('heading', 'highlighted_heading', 'subheading')
    ordering = ('order',)
    inlines = [SectionContentInline]

    fieldsets = (
        (None, {
            'fields': (
                'section_type', 'order', 'is_active',
                'super_heading', 'heading', 'highlighted_heading', 'subheading',
                'background_image', 'primary_image',
                'overlay_title', 'overlay_description',
                'primary_button_text', 'primary_button_url',
                'secondary_button_text', 'secondary_button_url',
            ),
        }),
    )

@admin.register(SectionContent)
class SectionContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'order', 'is_active')
    list_filter = ('section', 'is_active')
    search_fields = ('title', 'description', 'tags')
    ordering = ('section', 'order')
    fieldsets = (
        (None, {
            'fields': (
                'section', 'order', 'is_active',
                'icon', 'label', 'title', 'description', 'brochures',
                'tags', 'primary_button_text', 'primary_button_url',
                'question', 'answer',
            ),
        }),
    )
