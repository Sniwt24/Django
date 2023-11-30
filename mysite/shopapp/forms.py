from django import forms
from .models import Product, Order


# class CreateProductForm(forms.Form):
#     name = forms.CharField(label="Product name:", max_length=100)
#     description = forms.CharField(label="Desscription:", widget=forms.Textarea)
#     price = forms.DecimalField(label="Price ($):", decimal_places=2, min_value=1, max_value=100000)
#     discount = forms.IntegerField(label="Discount:", max_value=100, min_value=0)

class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "description", "price", "discount"


class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "delivery_address", "promocode", "user", "products"


class CSVImportForm(forms.Form):
    file = forms.FileField()
