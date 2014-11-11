from django import forms
from shop.models import PaymentMethod, Order


class ProcessOrderForm(forms.ModelForm):
	order_address = forms.CharField(max_length = 255, label = 'Shipping Address')
	order_payment_method = forms.ModelChoiceField(queryset = PaymentMethod.objects.all(), empty_label = 'Select One', label = 'Payment Method' )
	class Meta:
		model = Order
		exclude = ['user', 'order_date', 'order_status']