from django.contrib import admin
from .models import PageSection, SectionContent


class SectionContentInline(admin.StackedInline):
    model = SectionContent
    extra = 1
    fields = (
        'label', 'title', 'description', 'text',
        'question', 'answer', 'icon', 'order', 'is_active'
    )
    ordering = ('order',)


class PartnerContentInline(admin.StackedInline):
    model = SectionContent
    verbose_name = 'Partner'
    verbose_name_plural = 'Partners (add as many as needed)'
    extra = 1
    fields = ('title', 'icon', 'description', 'order', 'is_active')
    ordering = ('order', 'pk')

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'title':
            field.label = 'Partner name / logo alternative text'
            field.required = True
        elif db_field.name == 'icon':
            field.label = 'Partner logo'
            field.help_text = 'Upload a PNG, WebP or JPEG. Without a logo, the partner name is displayed.'
        elif db_field.name == 'description':
            field.help_text = 'Optional text displayed below this partner.'
        return field


@admin.register(PageSection)
class PageSectionAdmin(admin.ModelAdmin):
    list_display = (
        'section_type_display', 'content_object', 'order', 'is_active'
    )
    list_filter = ('section_type', 'is_active', 'content_type')
    search_fields = ('super_heading', 'heading', 'overview_text')
    ordering = ('order',)
    inlines = [SectionContentInline]
    readonly_fields = ('section_type_display',)

    def get_inlines(self, request, obj):
        if obj and obj.section_type == 'PARTNERS':
            return [PartnerContentInline]
        return super().get_inlines(request, obj)

    def get_fieldsets(self, request, obj=None):
        if obj and obj.section_type == 'PARTNERS':
            return [
                ('Partners strip', {
                    'fields': ('section_type_display', 'heading', 'subheading', 'is_active'),
                    'description': 'Heading and subheading control the collaborators text and partnership tagline. Manage logos and partner text below.',
                }),
                ('Section settings', {
                    'fields': ('section_type', 'content_type', 'object_id', 'order', 'label'),
                    'classes': ('collapse',),
                    'description': 'The homepage always places this strip between Hero and Overview.',
                }),
            ]
        return super().get_fieldsets(request, obj)

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

    def title_or_question(self, obj):
        return obj.title or obj.question or f"Content #{obj.id}"
    title_or_question.short_description = 'Title / Question'
