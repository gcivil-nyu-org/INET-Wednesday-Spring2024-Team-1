from rest_framework import serializers
from .models import Grocery, Ingredient


class GrocerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Grocery
        fields = ["gname", "price", "stock"]
        db_table = "groceryStore_grocery"

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["iid","iname", "price", "stock"]
        db_table = "groceryStore_ingredient"

class GroceryStockUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grocery
        fields = ["stock"]
