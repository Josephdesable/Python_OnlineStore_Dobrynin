# shop/views.py
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AddToCartForm
from .models import (
    Cart,
    InventoryItem,
    OrderItem,
    PurchaseOrder,
    ShoppingCartItem,
)


def product_list(request):
    products = InventoryItem.objects.filter(is_active=True)
    return render(request, "shop/product_list.html", {"products": products})


def product_detail(request, sku):
    # Обрати внимание: pk = sku (так как sku — primary_key)
    product = get_object_or_404(InventoryItem, sku=sku)
    return render(request, "shop/product_detail.html", {"product": product})
    
@login_required
def order_list(request):
    orders = PurchaseOrder.objects.filter(client=request.user).prefetch_related('orderitem_set__item')
    return render(request, "shop/orders/list.html", {"orders": orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(PurchaseOrder, id=order_id, client=request.user)
    return render(request, "shop/orders/detail.html", {"order": order})

@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(client=request.user)
    cart_items = ShoppingCartItem.objects.filter(cart=cart)

    if not cart_items:
        return redirect("cart")

    total = sum(item.item.price_rub * item.quantity for item in cart_items)

    if request.method == "POST":
        with transaction.atomic():
            # 1. Проверка остатков
            for item in cart_items:
                if item.item.stock_qty < item.quantity:
                    from django.contrib import messages
                    messages.error(
                        request,
                        f"Недостаточно товара {item.item.name} на складе. "
                        f"Доступно: {item.item.stock_qty}, запрошено: {item.quantity}."
                    )
                    return redirect("cart")

            # 2. Создание заказа
            order = PurchaseOrder.objects.create(
                client=request.user, total_rub=total, status="new"
            )

            # 3. Создание позиций + списание
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    item=item.item,
                    quantity=item.quantity,
                    price_at_order_rub=item.item.price_rub,
                )
                item.item.stock_qty -= item.quantity
                item.item.save(update_fields=["stock_qty"])

            # 4. Очистка корзины
            cart_items.delete()

            # 5. Успешный редирект — тоже внутри транзакции!
            return redirect("order_success")

    # GET-запрос: показать страницу оформления
    return render(
        request, "shop/checkout.html", {"cart_items": cart_items, "total": total}
    )
    

@login_required
def add_to_cart(request, sku):
    product = get_object_or_404(InventoryItem, sku=sku, is_active=True)
    cart, created = Cart.objects.get_or_create(client=request.user)

    if request.method == "POST":
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data["quantity"]

            # Если товара ещё нет в корзине — создаём с 0, чтобы потом прибавить
            cart_item, created = ShoppingCartItem.objects.get_or_create(
                cart=cart, item=product, defaults={"quantity": 0}
            )

            new_qty = cart_item.quantity + quantity
            
            # Проверяем СУММУ в корзине против остатка на складе
            if new_qty > product.stock_qty:
                form.add_error(
                    "quantity",
                    f"Недостаточно товара. На складе: {product.stock_qty}, уже в корзине: {cart_item.quantity}"
                )
            else:
                cart_item.quantity = new_qty  # ✅ Суммируем, а не перезаписываем
                cart_item.save()
                return redirect("cart")
    else:
        form = AddToCartForm()

    return render(request, "shop/add_to_cart.html", {"form": form, "product": product})
    

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(client=request.user)
    cart_items = ShoppingCartItem.objects.filter(cart=cart)

    total = sum(item.item.price_rub * item.quantity for item in cart_items)

    return render(request, "shop/cart.html", {"cart_items": cart_items, "total": total})







@login_required
def order_success(request):
    return render(request, "shop/order_success.html")
