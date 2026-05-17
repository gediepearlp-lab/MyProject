from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Supplier, InventoryItem, StockTransaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'email')
    search_fields = ('name', 'contact_person')


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'supplier', 'quantity', 'unit', 'cost_price', 'status')
    list_filter = ('category', 'supplier', 'unit')
    search_fields = ('name', 'sku')
    readonly_fields = ('created_at', 'updated_at', 'created_by')

    def status(self, obj):
        return obj.status
    status.short_description = 'Status'


@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ('item', 'transaction_type', 'quantity', 'created_by', 'created_at')
    list_filter = ('transaction_type',)
    readonly_fields = ('created_at', 'created_by')