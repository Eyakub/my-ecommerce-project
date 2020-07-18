from django.shortcuts import render
from django.contrib import messages

# models and forms
from app_order.models import Order
from app_payment.models import BillingAddress
from app_payment.forms import BillingForm

from django.contrib.auth.decorators import login_required


@login_required
def checkout(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    form = BillingForm(instance=saved_address)
    if request.method == 'POST':
        form = BillingForm(request.POST, instance=saved_address)
        if form.is_valid():
            form.save()
            form = BillingForm(instance=saved_address)
            messages.success(request, "Shipping address saved!")
    
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    print(order_qs)
    order_items = order_qs[0].order_items.all()
    print(order_items)
    order_total = order_qs[0].get_total()
    return render(request, 'app_payment/checkout.html', context={'form': form, "order_items": order_items, "order_total": order_total})