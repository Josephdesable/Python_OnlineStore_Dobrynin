# shop/forms.py

from django import forms
from .models import InventoryItem


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1, max_value=99, initial=1, label="Количество"
    )
