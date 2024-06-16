from django import forms
from .models import Delivery, Product

class DeliveryForm(forms.ModelForm):
    product_name = forms.CharField(max_length=255)
    product_description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Delivery
        fields = ['delivery_address', 'delivery_date', 'status']

    def save(self, commit=True, user=None):
        product = Product(
            name=self.cleaned_data['product_name'],
            description=self.cleaned_data['product_description'],
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
