from django.shortcuts import render, get_object_or_404, redirect

# authentications
from django.contrib.auth.decorators import login_required

# message
from django.contrib import messages

# model
from app_order.models import Cart, Order
from app_shop.models import Product


@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)
    
    """ 
    -> checking this order item already exist in Order model or not for that user
    -> order = false (that means only one order for that user at a time)
    -> order = order_qs[0] as filter returns list of queryset
    """
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item=item).exists():    # if item already exist in that order
            order_item[0].quantity += 1                     # increment the item quantity
            order_item[0].save()
            messages.info(request, "This item quantity was updated")
            return redirect("app_shop:home")
        else:
            order.order_items.add(order_item[0])
            messages.info(request, "This item was added to your cart")
            return redirect('app_shop:home')
    else:
        order = Order(user=request.user)
        order.save()
        order.order_items.add(order_item[0])
        messages.info(request, "This item was added to your cart")
        return redirect("app_shop:home")


@login_required
def cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)

    if carts.exists() and orders.exists():
        order = orders[0]
        return render(request, 'app_order/cart.html', context={'carts': carts, 'order': order})
    else:
        messages.warning(request, "You dont have any item in your cart")
        return redirect('app_shop:home')


@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        print('========>', order)
        if order.order_items.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            order.order_items.remove(order_item)
            order_item.delete()
            messages.warning(request, "This item was removed from your cart")
            return redirect('app_order:cart')
        else:
            messages.info(request, "This item was not in your cart")
            return redirect('app_shop:home')
    else:
        messages.info(request, "You don't have an active order")
        return redirect('app_shop:home')

    
@login_required
def increase_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if order_item.quantity >= 1:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, "{} quantity has been updated".format(item.name))
                return redirect('app_order:cart')
            else:
                messages.info(request, "{} quantity has been updated".format(item.name))
                return redirect('app_order:cart')
        else:
            messages.info(request, "{} is not in your cart".format(item.name))
    else:
        messages.info(request, "You don't have an active order")
        return redirect("app_shop:home")


@login_required
def decrease_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, "{} quantity has been updated".format(item.name))
                return redirect('app_order:cart')
            else:
                order.order_items.remove(order_item)
                order_item.delete()
                messages.info(request, "{} quantity has been updated".format(item.name))
                return redirect('app_order:cart')
        else:
            messages.info(request, "{} is not in your cart".format(item.name))
    else:
        messages.info(request, "You don't have an active order")
        return redirect("app_shop:home")