from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    price_cents = models.PositiveIntegerField()


    def price_display(self):
        return f"{self.price_cents/100:.2f}"


    def __str__(self):
        return self.name


class Order(models.Model):
    stripe_session_id = models.CharField(max_length=255, unique=True)
    total_cents = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


    def total_display(self):
        return f"{self.total_cents/100:.2f}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    unit_price_cents = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()


    def line_total_cents(self):
        return self.unit_price_cents * self.quantity
