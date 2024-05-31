from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'stock', 'pro_image', 'min_price', 'description', 'category']

    def clean_max_price(self):
        max_price = self.cleaned_data.get('max_price')
        if max_price is not None and max_price < self.instance.min_price:
            raise forms.ValidationError("Max price must be greater than or equal to the min price.")
        return max_price
    
class UpdateStatusForm(forms.Form):
    ORDER_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    ]

    new_status = forms.ChoiceField(choices=ORDER_STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))