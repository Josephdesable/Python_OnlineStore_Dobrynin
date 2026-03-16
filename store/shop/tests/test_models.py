from django.test import TestCase
from shop.models import InventoryItem, Cart, ShoppingCartItem
from users.models import User


class InventoryItemModelTest(TestCase):
    def test_create_inventory_item(self):
        item = InventoryItem.objects.create(
            sku="TST001",
            name="Футболка",
            description="Хлопковая футболка",
            price_rub=999.00,
            stock_qty=10
        )
        self.assertEqual(item.name, "Футболка")
        self.assertEqual(item.stock_qty, 10)
        self.assertTrue(item.is_active)

    def test_negative_stock_not_allowed(self):
        # PositiveIntegerField не позволяет сохранить отрицательное число
        with self.assertRaises(ValueError):
            InventoryItem.objects.create(
                sku="TST002",
                name="Невидимка",
                description="Тест",
                price_rub=1.00,
                stock_qty=-5
            )


class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="pass123"
        )

    def test_cart_creation(self):
        cart = Cart.objects.create(client=self.user)
        self.assertEqual(cart.client, self.user)
        self.assertIsNotNone(cart.created_at)


from django.test import TestCase
from django.db import IntegrityError
from shop.models import InventoryItem


class InventoryItemModelTest(TestCase):
    def test_create_inventory_item(self):
        item = InventoryItem.objects.create(
            sku="TST001",
            name="Футболка",
            description="Хлопковая футболка",
            price_rub=999.00,
            stock_qty=10
        )
        self.assertEqual(item.name, "Футболка")
        self.assertEqual(item.stock_qty, 10)
        self.assertTrue(item.is_active)

    def test_negative_stock_not_allowed(self):
        with self.assertRaises(IntegrityError):
            InventoryItem.objects.create(
                sku="TST002",
                name="Невидимка",
                description="Тест",
                price_rub=1.00,
                stock_qty=-5
            )
