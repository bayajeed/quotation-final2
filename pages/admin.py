from django.contrib import admin
from .models import (
    Quotation, QuotationGroup, QuotationItem,
    QuotationTemplate, QuotationTemplateItem,
    Item, ItemGroup, Unit
)


class QuotationItemInline(admin.TabularInline):
    model = QuotationItem
    extra = 1
    autocomplete_fields = ['item']


class QuotationGroupInline(admin.TabularInline):
    model = QuotationGroup
    extra = 1


@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ('title', 'client_name', 'created_at', 'total_amount')
    inlines = [QuotationGroupInline]
    search_fields = ('title', 'client_name')


@admin.register(QuotationGroup)
class QuotationGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'quotation', 'subtotal')
    inlines = [QuotationItemInline]
    search_fields = ('name',)


class QuotationTemplateItemInline(admin.TabularInline):
    model = QuotationTemplateItem
    extra = 1
    fields = ('item', 'qty', 'unit_price')
    autocomplete_fields = ['item']


@admin.register(QuotationTemplate)
class QuotationTemplateAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [QuotationTemplateItemInline]
    search_fields = ('name',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'unit', 'unit_price')
    search_fields = ('name', 'description')
    list_filter = ('group', 'unit')


admin.site.register(Unit)
admin.site.register(ItemGroup)