from django.db import models
from django.contrib.auth.models import User


class Grocery(models.Model):
    gid = models.AutoField(primary_key=True)
    gname = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.gname


class Order(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]
    oid = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    calories = models.IntegerField()
    recipe = models.TextField()

    def __str__(self):
        return (
            f"Order ID: {self.oid}, User: {self.user.username}, Status: {self.status}"
        )


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    grocery = models.ForeignKey(Grocery, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"Order ID: {self.order.oid}, Grocery: {self.grocery.gname}, Quantity: {self.quantity}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=20)
    addr = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.user.username
