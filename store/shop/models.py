# shop/models.py

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

# shop/models.py


User = get_user_model()


class Cart(models.Model):
    """Корзина покупателя"""

    client = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Клиент")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"Корзина {self.client.username}"


class InventoryItem(models.Model):
    sku = models.CharField(max_length=50, primary_key=True, verbose_name="Артикул")
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(
        upload_to="products/", blank=True, null=True, verbose_name="Изображение"
    )
    price_rub = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена (руб)"
    )
    stock_qty = models.PositiveIntegerField(default=0, verbose_name="Остаток на складе")
    is_active = models.BooleanField(default=True, verbose_name="В продаже")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлен")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.sku})"


class ShoppingCartItem(models.Model):
    """Товар в корзине клиента"""

    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, verbose_name="Корзина", null=True
    )
    item = models.ForeignKey(
        InventoryItem, on_delete=models.CASCADE, verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"
        unique_together = ("cart", "item")

    def __str__(self):
        return (
            f"{self.item.name} × {self.quantity} (в корзине {self.cart.user.username})"
        )


class PurchaseOrder(models.Model):
    """Заказ клиента"""

    STATUS_CHOICES = [
        ("new", "Новый"),
        ("confirmed", "Подтверждён"),
        ("shipped", "Отправлен"),
        ("delivered", "Доставлен"),
        ("cancelled", "Отменён"),
    ]

    client = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, verbose_name="Клиент"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="new", verbose_name="Статус"
    )
    total_rub = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Сумма заказа (руб)"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлён")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заказ №{self.id} от {self.client.username}"


class OrderItem(models.Model):
    """Позиция в заказе"""

    order = models.ForeignKey(
        PurchaseOrder, on_delete=models.CASCADE, verbose_name="Заказ"
    )
    item = models.ForeignKey(
        InventoryItem, on_delete=models.PROTECT, verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    price_at_order_rub = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена на момент заказа"
    )

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    def __str__(self):
        return f"{self.item.name} × {self.quantity} в {self.order}"
