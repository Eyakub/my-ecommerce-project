from django import forms
from app_payment.models import BillingAddress


class BillingForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = ['address', 'zipcode', 'city', 'country']