from django.contrib import admin
from .models import PageSection, SectionContent


class SectionContentInline(admin.StackedInline):
    model = SectionContent
    extra = 1
    fields = (
        'icon',
        'title',
        'description',
        'label_1',
        'label_2',
        'tags',
        'order',
        'is_active',
    )
    ordering = ('order',)


@admin.register(PageSection)
class PageSectionAdmin(admin.ModelAdmin):
    list_display = (
        'section_type_display',
        'submenu',
        'order',
        'is_active',
    )
    list_filter = ('section_type', 'is_active', 'submenu')
    search_fields = ('super_heading', 'heading', 'highlighted_heading_text')
    ordering = ('submenu', 'order')
    inlines = [SectionContentInline]
    readonly_fields = ('section_type_display',)

    def section_type_display(self, obj):
        return obj.get_section_type_display()
    section_type_display.short_description = 'Section Type'


@admin.register(SectionContent)
class SectionContentAdmin(admin.ModelAdmin):
    list_display = (
        'section',
        'title_or_id',
        'order',
        'is_active',
    )
    list_filter = ('is_active', 'section__section_type')
    search_fields = ('title', 'description', 'tags')
    ordering = ('section', 'order')

    def title_or_id(self, obj):
        return obj.title or f"Content #{obj.id}"
    title_or_id.short_description = 'Title'
    