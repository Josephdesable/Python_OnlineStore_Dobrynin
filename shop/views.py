# shop/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import InventoryItem, ShoppingCartItem, Cart
from .forms import AddToCartForm


def product_list(request):
    products = InventoryItem.objects.filter(is_active=True)
    return render(request, "shop/product_list.html", {"products": products})


def product_detail(request, sku):
    # Обрати внимание: pk = sku (так как sku — primary_key)
    product = get_object_or_404(InventoryItem, sku=sku)
    return render(request, "shop/product_detail.html", {"product": product})


@login_required
def add_to_cart(request, sku):
    product = get_object_or_404(InventoryItem, sku=sku, is_active=True)

    cart, created = Cart.objects.get_or_create(client=request.user)

    if request.method == "POST":
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data["quantity"]
            if quantity > product.stock_qty:
                form.add_error(
                    "quantity", f"Недостаточно товара. В наличии: {product.stock_qty}"
                )
            else:

                cart_item, created = ShoppingCartItem.objects.get_or_create(
                    cart=cart, item=product, defaults={"quantity": quantity}
                )
                if not created:
                    cart_item.quantity = quantity
                    cart_item.save()
                return redirect("cart")
    else:
        form = AddToCartForm()

    return render(request, "shop/add_to_cart.html", {"form": form, "product": product})


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(client=request.user)
    cart_items = ShoppingCartItem.objects.filter(cart=cart)  # ← фильтруем по cart

    total = sum(item.item.price_rub * item.quantity for item in cart_items)

    return render(request, "shop/cart.html", {"cart_items": cart_items, "total": total})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, ShoppingCartItem, PurchaseOrder, OrderItem


@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(client=request.user)
    cart_items = ShoppingCartItem.objects.filter(cart=cart)

    if not cart_items:
        return redirect("cart")

    # Считаем итоговую сумму
    total = sum(item.item.price_rub * item.quantity for item in cart_items)

    if request.method == "POST":

        order = PurchaseOrder.objects.create(
            client=request.user, total_rub=total, status="new"
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                item=item.item,
                quantity=item.quantity,
                price_at_order_rub=item.item.price_rub,
            )

        cart_items.delete()

        return redirect("order_success")

    return render(
        request, "shop/checkout.html", {"cart_items": cart_items, "total": total}
    )


@login_required
def order_success(request):
    return render(request, "shop/order_success.html")
