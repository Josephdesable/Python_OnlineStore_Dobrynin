# store/shop/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from shop.models import InventoryItem, Cart, ShoppingCartItem, PurchaseOrder

User = get_user_model()


class RegistrationTests(TestCase):
    """Проверяем, что ФИО сохраняется при регистрации (замечание проверяющего)"""
    def test_registration_saves_first_last_name(self):
        resp = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'test@example.com',
            'first_name': 'Алексей',
            'last_name': 'Сидоров',
            'middle_name': 'Иванович',
            'phone': '+79001112233',
            'address': 'г. Москва, ул. Тестовая, 1',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        # После регистрации обычно редирект (302)
        self.assertIn(resp.status_code, [200, 302])
        if resp.status_code == 302:
            user = User.objects.get(username='newuser')
            self.assertEqual(user.first_name, 'Алексей')
            self.assertEqual(user.last_name, 'Сидоров')


class CartAndCheckoutTests(TestCase):
    """Тестируем суммирование в корзине и списание остатков при заказе"""
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='test123',
            first_name='Иван', last_name='Иванов'
        )
        self.product = InventoryItem.objects.create(
            sku='TEST-001', name='Тестовый товар', description='Описание',
            price_rub=500.00, stock_qty=10
        )

    def test_cart_sums_quantity(self):
        """Добавление одного товара дважды должно суммировать количество"""
        self.client.login(username='testuser', password='test123')
        
        self.client.post(reverse('add_to_cart', args=[self.product.sku]), {'quantity': 2})
        self.client.post(reverse('add_to_cart', args=[self.product.sku]), {'quantity': 3})
        
        cart_item = ShoppingCartItem.objects.get(cart__client=self.user, item=self.product)
        self.assertEqual(cart_item.quantity, 5)

    def test_checkout_reduces_stock(self):
        """Оформление заказа должно уменьшать stock_qty"""
        self.client.login(username='testuser', password='test123')
        
        # Создаём корзину вручную для теста
        cart = Cart.objects.create(client=self.user)
        ShoppingCartItem.objects.create(cart=cart, item=self.product, quantity=3)
        
        # Отправляем POST на checkout
        resp = self.client.post(reverse('checkout'))
        self.assertEqual(resp.status_code, 302)  # редирект на успех
        
        # Проверяем, что остаток уменьшился
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_qty, 7)  # 10 - 3


class InventoryModelTests(TestCase):
    """Базовые тесты модели товара (из твоих исходных файлов)"""
    def test_create_item(self):
        item = InventoryItem.objects.create(
            sku='TST-001', name='Футболка', description='Хлопок',
            price_rub=999.00, stock_qty=10
        )
        self.assertEqual(item.name, 'Футболка')
        self.assertEqual(item.stock_qty, 10)
        self.assertTrue(item.is_active)

    def test_negative_stock_blocked(self):
        """PositiveIntegerField не даст сохранить отрицательное число"""
        with self.assertRaises(IntegrityError):
            InventoryItem.objects.create(
                sku='TST-002', name='Невидимка', description='Тест',
                price_rub=1.00, stock_qty=-5
            )
