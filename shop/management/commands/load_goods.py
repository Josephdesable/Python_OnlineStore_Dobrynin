# shop/management/commands/load_goods.py

import csv

from django.core.management.base import BaseCommand
from shop.models import InventoryItem


class Command(BaseCommand):
    help = "Загружает товары из CSV"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Путь к CSV-файлу")

    def handle(self, *args, **options):
        file_path = options["file_path"]
        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                InventoryItem.objects.update_or_create(
                    sku=row["Артикул"],
                    defaults={
                        "name": row["Название"],
                        "price_rub": row["Цена"],
                        "stock_qty": row["Остаток"],
                        "is_active": True,
                    },
                )
        self.stdout.write(self.style.SUCCESS("Товары загружены!"))
