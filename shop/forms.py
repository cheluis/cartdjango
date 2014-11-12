from django import forms
from shop.models import PaymentMethod, Order, Publication


class ProcessOrderForm(forms.ModelForm):
	order_address = forms.CharField(max_length = 255, label = 'Shipping Address')
	order_payment_method = forms.ModelChoiceField(queryset = PaymentMethod.objects.all(), empty_label = 'Select One', label = 'Payment Method' )
	order_payment_number = forms.CharField(max_length = 20, label = 'Card Number')
	class Meta:
		model = Order
		exclude = ['user', 'order_date', 'order_status']

class OrderDetailForm(forms.Form):
	order_quantity = forms.IntegerField(label = 'Quantity', min_value=1)
	order_presentation = forms.ModelChoiceField(queryset = None, empty_label = 'Select One', label = 'Product Presentation' )