from django.contrib import admin
from .models import PageSection, SectionContent


class SectionContentInline(admin.StackedInline):
    model = SectionContent
    extra = 1
    fields = (
        'label', 'title', 'description', 'text',
        'question', 'answer', 'icon',
        'primary_button_text', 'primary_button_url',
        'secondary_button_text', 'secondary_button_url',
        'order', 'is_active'
    )
    ordering = ('order',)


@admin.register(PageSection)
class PageSectionAdmin(admin.ModelAdmin):
    list_display = (
        'section_type_display', 'order', 'is_active'
    )
    list_filter = ('section_type', 'is_active',)
    search_fields = ('super_heading', 'heading', 'overview_text')
    ordering = ('order',)
    inlines = [SectionContentInline]
    readonly_fields = ('section_type_display',)

    def section_type_display(self, obj):
        return obj.get_section_type_display()
    section_type_display.short_description = 'Section Type'


@admin.register(SectionContent)
class SectionContentAdmin(admin.ModelAdmin):
    list_display = (
        'section', 'title_or_question', 'order', 'is_active'
    )
    list_filter = ('is_active', 'section')
    search_fields = (
        'label', 'title', 'description', 'text', 'question', 'answer'
    )
    ordering = ('section', 'order')

    # Just add the button fields to the default form display
    fields = (
        'section', 'label', 'title', 'description', 'text',
        'question', 'answer', 'icon',
        'primary_button_text', 'primary_button_url',
        'secondary_button_text', 'secondary_button_url',
        'order', 'is_active'
    )

    def title_or_question(self, obj):
        return obj.title or obj.question or f"Content #{obj.id}"
    title_or_question.short_description = 'Title / Question'
