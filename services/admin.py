from django.contrib import admin
from django.utils.html import format_html
from .models import Partner, Service, ServicesPage, ValuePillar


@admin.register(ServicesPage)
class ServicesPageAdmin(admin.ModelAdmin):
    readonly_fields = ('hero_image_preview',)
    fieldsets = (
        ('Hero & alliance', {'fields': ('eyebrow', 'heading', 'subheading', 'partner_tags')}),
        ('Hero photography', {'fields': ('hero_image', 'hero_image_preview', 'hero_image_alt', 'hero_image_caption', 'hero_image_position')}),
        ('Corporate inquiries', {'fields': ('inquiry_heading', 'contact_name', 'contact_role', 'primary_phone', 'secondary_phone', 'whatsapp_phone', 'location')}),
    )

    def has_add_permission(self, request):
        return not ServicesPage.objects.exists() and super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description='Current hero image')
    def hero_image_preview(self, obj):
        if not obj or not obj.hero_image:
            return 'No image selected. The alliance blueprint will be shown.'
        return format_html('<img src="{}" alt="{}" style="width:240px;height:160px;object-fit:cover;object-position:{};border-radius:4px">', obj.hero_image.url, obj.hero_image_alt, obj.hero_image_position)


class OrderedAdmin(admin.ModelAdmin):
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)


@admin.register(Partner)
class PartnerAdmin(OrderedAdmin):
    list_display = ('code', 'name', 'order', 'is_active')
    search_fields = ('code', 'name')


@admin.register(Service)
class ServiceAdmin(OrderedAdmin):
    list_display = ('title', 'audience', 'order', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description')
    readonly_fields = ('image_preview',)
    fieldsets = (
        ('Service content', {'fields': ('title', 'slug', 'short_title', 'audience', 'description', 'outcome', 'specs', 'deliverables')}),
        ('Service photography', {'fields': ('image', 'image_preview', 'image_alt', 'image_caption', 'image_position')}),
        ('Publishing', {'fields': ('order', 'is_active')}),
    )

    @admin.display(description='Current service image')
    def image_preview(self, obj):
        if not obj or not obj.image:
            return 'No image selected. This service will use the text layout.'
        return format_html('<img src="{}" alt="{}" style="width:240px;height:160px;object-fit:cover;object-position:{};border-radius:4px">', obj.image.url, obj.image_alt, obj.image_position)


@admin.register(ValuePillar)
class ValuePillarAdmin(OrderedAdmin):
    list_display = ('title', 'metric', 'order', 'is_active')
