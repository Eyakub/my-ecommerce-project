from django.db import models
from django.conf import settings

# models
from app_shop.models import Product


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} x {}".format(self.quantity, self.item)
    
    def get_total(self):
        total = self.item.price * self.quantity
        float_total = format(total, '0.3f')
        return float_total


class Order(models.Model):
    order_items = models.ManyToManyField(Cart)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order')
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    paymentId = models.CharField(max_length=264, blank=True, null=True)
    orderId = models.CharField(max_length=200, blank=True, null=True)

    def get_total(self):
        total = 0
        for order_item in self.order_items.all():
            total += float(order_item.get_total())
        return total