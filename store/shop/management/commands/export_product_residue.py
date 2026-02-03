# shop/management/commands/export_product_residue.py

import csv

from django.core.management.base import BaseCommand
from shop.models import InventoryItem


class Command(BaseCommand):
    help = "Выгружает остатки товаров в CSV"

    def handle(self, *args, **options):
        with open("stock_balance.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Артикул", "Название", "Остаток", "Цена"])
            for item in InventoryItem.objects.all():
                writer.writerow([item.sku, item.name, item.stock_qty, item.price_rub])
        self.stdout.write(self.style.SUCCESS("Остатки выгружены в stock_balance.csv"))
