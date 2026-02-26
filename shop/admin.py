from django.contrib import admin
from .models import Product, Order, OrderItem, Receipt, Report
from django.urls import reverse
from django.utils.html import format_html


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "subcategory", "price", "stock")
    list_filter = ("category", "subcategory")
    search_fields = ("name", "subcategory")
    list_editable = ("stock",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "price", "size", "get_total")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "tracking_number",
        "buyer",
        "display_amount",
        "delivery_fee",
        "status",
        "mpesa_receipt",
        "phone",
    )
    list_filter = ("status",)
    search_fields = ("tracking_number", "buyer__username", "mpesa_receipt", "phone")
    readonly_fields = ("tracking_number", "display_amount")
    inlines = [OrderItemInline]

    def display_amount(self, obj):
        return obj.get_total_amount()

    display_amount.short_description = "Amount"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["inventory_url"] = reverse("inventory")
        return super().changelist_view(request, extra_context)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price", "size", "get_total")
    list_filter = ("product",)
    search_fields = ("order__tracking_number", "product__name")


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ("receipt_number", "order", "generated_at")
    search_fields = ("receipt_number", "order__tracking_number")
    readonly_fields = ("receipt_number", "order", "generated_at")


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("title", "report_type", "generated_at")
    list_filter = ("report_type",)
    readonly_fields = ("report_type", "title", "generated_at", "data")


admin.site.site_header = "FashionHub Administration"
admin.site.site_title = "FashionHub Admin"
admin.site.index_title = "Welcome to FashionHub Admin Panel"
