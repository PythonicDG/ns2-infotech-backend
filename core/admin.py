from django.contrib import admin
from .models import (
    Menu,
    SubMenu,
    FooterSection,
    FooterItem,
    FooterSubscription,
    CompanyProfile,
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
