from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from .models import (
    PageSection, HeroSection, OverviewSection, WhyChooseUsSection,
    OurServicesSection, PlacementSection, TestimonialSection,
    FaqSection, ContactUsSection, CtaSection, SectionContent
)


class SectionContentInline(admin.StackedInline):
    model = SectionContent
    extra = 1
    fieldsets = (
        ('General Content', {
            'fields': ('label', 'title', 'description', 'text', 'icon')
        }),
        ('FAQ Specific', {
            'fields': ('question', 'answer'),
            'classes': ('collapse',),
            'description': 'Only fill these if the section is an FAQ.'
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
    )
    ordering = ('order',)


class BaseSectionChildAdmin(PolymorphicChildModelAdmin):
    """Base admin for all specific section types"""
    base_model = PageSection
    inlines = [SectionContentInline]


@admin.register(HeroSection)
class HeroSectionAdmin(BaseSectionChildAdmin):
    base_model = HeroSection
    show_in_index = True
    fieldsets = (
        ('Internal Name', {'fields': ('label',)}),
        ('Main Content', {'fields': ('super_heading', 'heading', 'subheading', 'overview_text')}),
        ('Media', {'fields': ('background_image',)}),
        ('Buttons', {'fields': (
            ('primary_button_text', 'primary_button_url'),
            ('secondary_button_text', 'secondary_button_url')
        )}),
        ('Visibility', {'fields': ('order', 'is_active')}),
    )


@admin.register(OverviewSection)
class OverviewSectionAdmin(BaseSectionChildAdmin):
    base_model = OverviewSection
    show_in_index = True
    fieldsets = (
        ('Internal Name', {'fields': ('label',)}),
        ('Main Content', {'fields': ('heading', 'subheading')}),
        ('Media & Badge', {'fields': ('primary_image', 'overview_text')}),
        ('Buttons', {'fields': (
            ('primary_button_text', 'primary_button_url'),
            ('secondary_button_text', 'secondary_button_url')
        )}),
        ('Visibility', {'fields': ('order', 'is_active')}),
    )


@admin.register(WhyChooseUsSection)
class WhyChooseUsSectionAdmin(BaseSectionChildAdmin):
    base_model = WhyChooseUsSection
    show_in_index = True


@admin.register(OurServicesSection)
class OurServicesSectionAdmin(BaseSectionChildAdmin):
    base_model = OurServicesSection
    show_in_index = True


@admin.register(PlacementSection)
class PlacementSectionAdmin(BaseSectionChildAdmin):
    base_model = PlacementSection
    show_in_index = True


@admin.register(TestimonialSection)
class TestimonialSectionAdmin(BaseSectionChildAdmin):
    base_model = TestimonialSection
    show_in_index = True


@admin.register(FaqSection)
class FaqSectionAdmin(BaseSectionChildAdmin):
    base_model = FaqSection
    show_in_index = True


@admin.register(ContactUsSection)
class ContactUsSectionAdmin(BaseSectionChildAdmin):
    base_model = ContactUsSection
    show_in_index = True


@admin.register(CtaSection)
class CtaSectionAdmin(BaseSectionChildAdmin):
    base_model = CtaSection
    show_in_index = True
    fieldsets = (
        ('Internal Name', {'fields': ('label',)}),
        ('Main Content', {'fields': ('heading', 'subheading')}),
        ('Button', {'fields': (('primary_button_text', 'primary_button_url'),)}),
        ('Visibility', {'fields': ('order', 'is_active')}),
    )


@admin.register(PageSection)
class PageSectionAdmin(PolymorphicParentModelAdmin):
    """The parent model admin that handles the routing to child admins"""
    base_model = PageSection
    child_models = (
        HeroSection, OverviewSection, WhyChooseUsSection,
        OurServicesSection, PlacementSection, TestimonialSection,
        FaqSection, ContactUsSection, CtaSection
    )
    list_display = ('label', 'polymorphic_ctype', 'order', 'is_active')
    list_filter = (PolymorphicChildModelFilter, 'is_active')
    ordering = ('order',)


@admin.register(SectionContent)
class SectionContentAdmin(admin.ModelAdmin):
    list_display = ('section', 'title_or_question', 'order', 'is_active')
    list_filter = ('is_active', 'section')
    search_fields = ('label', 'title', 'description', 'text', 'question', 'answer')

    def title_or_question(self, obj):
        return obj.title or obj.question or f"Content #{obj.id}"
    title_or_question.short_description = 'Title / Question'
