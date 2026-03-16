# store/shop/tests/test_unit.py

from django.test import TestCase
from django.core.exceptions import ValidationError
from shop.utils import add_to_cart, submit_order, get_cart_contents, get_unshipped_orders
from shop.models import InventoryItem, Cart, ShoppingCartItem, PurchaseOrder
from users.models import User


class OrderSubmissionUnitTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass")
        self.order = PurchaseOrder.objects.create(
            client=self.user,
            status="new",
            total_rub=1000.00
        )

    def test_submit_order_success(self):
        order = submit_order(self.order)
        self.assertEqual(order.status, "confirmed")

    def test_submit_non_new_order_fails(self):
        self.order.status = "confirmed"
        self.order.save()
        with self.assertRaises(ValueError):
            submit_order(self.order)


class CartOperationsUnitTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass")
        self.cart = Cart.objects.create(client=self.user)
        self.item = InventoryItem.objects.create(
            sku="TST001",
            name="Футболка",
            description="Хлопок",
            price_rub=999.00,
            stock_qty=10
        )

    def test_add_to_cart_success(self):
        cart_item = add_to_cart(self.cart, self.item, 3)
        self.assertEqual(cart_item.quantity, 3)
        self.assertEqual(ShoppingCartItem.objects.count(), 1)

    def test_add_to_cart_exceeds_stock(self):
        with self.assertRaises(ValueError):
            add_to_cart(self.cart, self.item, 15)  # больше, чем stock_qty=10

    def test_add_to_cart_twice(self):
        add_to_cart(self.cart, self.item, 2)
        add_to_cart(self.cart, self.item, 3)
        cart_item = ShoppingCartItem.objects.get(cart=self.cart, item=self.item)
        self.assertEqual(cart_item.quantity, 5)

    def test_get_cart_contents(self):
        add_to_cart(self.cart, self.item, 2)
        contents = get_cart_contents(self.cart)
        self.assertEqual(len(contents), 1)
        self.assertEqual(contents[0]["name"], "Футболка")
        self.assertEqual(contents[0]["quantity"], 2)


class UnshippedOrdersTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass")
        PurchaseOrder.objects.create(client=self.user, status="new", total_rub=100)
        PurchaseOrder.objects.create(client=self.user, status="confirmed", total_rub=200)
        PurchaseOrder.objects.create(client=self.user, status="shipped", total_rub=300)

    def test_get_unshipped_orders(self):
        orders = get_unshipped_orders()
        self.assertEqual(orders.count(), 2)
        statuses = set(order.status for order in orders)
        self.assertEqual(statuses, {"new", "confirmed"})
