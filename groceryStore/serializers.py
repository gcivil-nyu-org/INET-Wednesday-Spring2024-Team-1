from rest_framework import serializers
from .models import Grocery


class GrocerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Grocery
        fields = ["gname", "price", "stock"]
        db_table = "groceryStore_grocery"


class GroceryStockUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grocery
        fields = ['stock']