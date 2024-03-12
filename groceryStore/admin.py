from django.contrib import admin
from .models import Grocery, Order, OrderItem, UserProfile


admin.site.register(Grocery)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(UserProfile)
