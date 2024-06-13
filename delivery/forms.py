from django import forms
from .models import Delivery, Product

class DeliveryForm(forms.ModelForm):
    product_name = forms.CharField(max_length=255)
    product_description = forms.CharField(widget=forms.Textarea)
    product_price = forms.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Delivery
        fields = ['delivery_address', 'delivery_date', 'status']

    def save(self, commit=True, user=None):
        product = Product(
            name=self.cleaned_data['product_name'],
            description=self.cleaned_data['product_description'],
            price=self.cleaned_data['product_price'],
        )
        if commit:
            product.save()
        delivery = super().save(commit=False)
        delivery.product = product
        if user:
            delivery.user = user
        if commit:
            delivery.save()
        return delivery
