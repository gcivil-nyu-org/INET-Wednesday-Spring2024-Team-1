from django.shortcuts import render
from django.http import HttpResponse
from .models import Grocery, Order, OrderItem, UserProfile, Ingredient
from users.models import CustomUser, CartData
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import (
    GrocerySerializer,
    GroceryStockUpdateSerializer,
    IngredientSerializer,
    OrderSerializer,
)
from django.http import JsonResponse


# Create your views here.

@api_view(["GET"])
def get_grocery_details(request, grocery_id):
    try:
        # Fetch the grocery data using the provided gname from the groceryStore_grocery table
        # grocery = Grocery.objects.using("groceryStore_grocery").get(gname=gname)
        ingredient = Ingredient.objects.get(iid=grocery_id)
        # Serialize the grocery data
        serializer = IngredientSerializer(ingredient)
        # Return the serialized data in the response
        return Response(serializer.data)
    except Ingredient.DoesNotExist:
        # Return a 404 response if the grocery with the provided gname doesn't exist
        return Response({"message": "Grocery not found"}, status=404)


@api_view(["POST"])
def get_order_data(request):
    username = request.data.get("username", None)
    if username is not None:
        user = get_object_or_404(User, username=username)
        orders = Order.objects.filter(user=user).prefetch_related("orderitem_set")
        serializer = OrderSerializer(orders, many=True, context={"request": request})
        return Response(serializer.data)
    else:
        return Response({"error": "No modi provided"}, status=400)


@api_view(["PUT"])
def place_order(request):
    if request.method == "PUT":
        print("Request Data: ", request.data)
        username = request.user.username
        print("Username: ", username)
        items = request.data["items"].values()
        user = get_object_or_404(User, username=username)
        order = Order.objects.create(user=user)

        # For each item, create a new OrderItem instance linked to the order
        for item in items:
            grocery_id = item["id"]
            quantity = item["quantity"]

            # Get the Grocery instance for the grocery_id
            grocery = get_object_or_404(Ingredient, iid=grocery_id)

            # Create a new OrderItem instance
            OrderItem.objects.create(order=order, grocery=grocery, quantity=quantity)
        custom_user = CustomUser.objects.get(email=request.user.email)
        print("Custom user:", custom_user)
        cart_data_obj = CartData.objects.filter(user=custom_user).first()
        # Clear the cart data
        if cart_data_obj:
            cart_data_obj.delete()

        return Response({"message": "Order placed successfully"})
    return Response({"message": "Invalid request method"}, status=400)


@api_view(["PUT"])
def update_grocery_stock(request, gname):
    try:
        grocery = Grocery.objects.get(gname=gname)
    except Grocery.DoesNotExist:
        return Response({"message": "Grocery not found"}, status=404)

    if request.method == "PUT":
        serializer = GroceryStockUpdateSerializer(instance=grocery, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


def clear_cart_data(request):
    if "cart_data" in request.session:
        del request.session["cart_data"]
    return JsonResponse({"status": "success"})
