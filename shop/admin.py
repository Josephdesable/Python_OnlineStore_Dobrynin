# shop/admin.py

from django.contrib import admin
from .models import InventoryItem, ShoppingCartItem, PurchaseOrder, OrderItem, Cart


# Товары
@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ["sku", "name", "price_rub", "stock_qty", "is_active", "image"]
    list_filter = ["is_active"]
    search_fields = ["sku", "name"]
    list_editable = ["price_rub", "stock_qty", "is_active"]


@admin.register(ShoppingCartItem)
class ShoppingCartItemAdmin(admin.ModelAdmin):
    list_display = ["cart", "item", "quantity"]  # ← заменили client на cart
    list_filter = ["cart__client"]  # ← фильтруем по клиенту через корзину
    search_fields = ["cart__client__username", "item__name"]


# Заказы
@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ["id", "client", "status", "total_rub", "created_at"]
    list_filter = ["status", "created_at"]
    readonly_fields = ["created_at", "updated_at"]


# Позиции заказа
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "item", "quantity", "price_at_order_rub"]
    list_filter = ["order__client"]


# shop/admin.py


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["client", "created_at"]
    search_fields = ["client__username"]
