from django.contrib import admin
from .models import PageSection, SectionContent


class SectionContentInline(admin.StackedInline):
    model = SectionContent
    extra = 1
    fields = (
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
    )
    ordering = ['order']
    show_change_link = True


@admin.register(PageSection)
class PageSectionAdmin(admin.ModelAdmin):
    list_display = ('section_type', 'order', 'is_active')
    list_filter = ('section_type', 'is_active')
    search_fields = ('heading', 'subheading', 'overview_text')
    ordering = ['order']

    inlines = [SectionContentInline]

    fieldsets = (
        ('Section Info', {
            'fields': ('section_type', 'order', 'is_active')
        }),
        ('Headings and Texts', {
            'fields': ('super_heading', 'heading', 'subheading', 'overview_text')
        }),
        ('Images', {
            'fields': ('background_image', 'primary_image')
        }),
        ('Primary CTA Button', {
            'fields': ('primary_button_text', 'primary_button_url')
        }),
        ('Secondary CTA Button', {
            'fields': ('secondary_button_text', 'secondary_button_url')
        }),
    )


@admin.register(SectionContent)
class SectionContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'person_name', 'order', 'section', 'is_active')
    list_filter = ('is_active', 'section')
    search_fields = ('title', 'description', 'person_name', 'person_role')
    ordering = ['section', 'order']
