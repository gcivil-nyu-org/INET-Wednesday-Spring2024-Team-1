from rest_framework import serializers
<<<<<<< HEAD
from .models import Grocery
=======
from .models import Grocery, Ingredient, Order, OrderItem
>>>>>>> develop


class GrocerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Grocery
        fields = ["gname", "price", "stock"]
        db_table = "groceryStore_grocery"


<<<<<<< HEAD
=======
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["iid", "iname", "price", "stock"]
        db_table = "groceryStore_ingredient"


>>>>>>> develop
class GroceryStockUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grocery
        fields = ["stock"]
<<<<<<< HEAD
=======


class OrderItemSerializer(serializers.ModelSerializer):
    # grocery_detail = serializers.HyperlinkedIdentityField(
    #     view_name='get_grocery_details',  # Replace with the name of your grocery details view
    #     lookup_field='grocery_id'
    # )
    grocery = IngredientSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["order_id", "grocery", "quantity"]
        db_table = "groceryStore_orderitem"


class OrderSerializer(serializers.ModelSerializer):
    orderitem_set = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["oid", "date", "status", "user", "calories", "orderitem_set"]
        db_table = "groceryStore_order"
>>>>>>> develop
