# store/shop/utils.py

from .models import ShoppingCartItem, PurchaseOrder


def add_to_cart(cart, item, quantity):
    """Добавить товар в корзину. Возвращает объект ShoppingCartItem."""
    if quantity <= 0:
        raise ValueError("Количество должно быть положительным.")
    if quantity > item.stock_qty:
        raise ValueError("Недостаточно товара на складе.")

    cart_item, created = ShoppingCartItem.objects.get_or_create(
        cart=cart,
        item=item,
        defaults={"quantity": quantity}
    )
    if not created:
        new_quantity = cart_item.quantity + quantity
        if new_quantity > item.stock_qty:
            raise ValueError("Недостаточно товара на складе.")
        cart_item.quantity = new_quantity
        cart_item.save()
    return cart_item


def submit_order(order):
    """Оформить заказ: изменить статус на 'confirmed'."""
    if order.status != "new":
        raise ValueError("Можно подтвердить только новый заказ.")
    order.status = "confirmed"
    order.save()
    return order


def get_cart_contents(cart):
    """Получить содержимое корзины как список словарей."""
    items = ShoppingCartItem.objects.filter(cart=cart)
    return [
        {
            "item_id": item.item.sku,
            "name": item.item.name,
            "quantity": item.quantity,
            "price": float(item.item.price_rub),
        }
        for item in items
    ]


def get_unshipped_orders():
    """Получить все неотправленные заказы."""
    return PurchaseOrder.objects.filter(status__in=["new", "confirmed"])
