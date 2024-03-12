from django.shortcuts import render
from django.http import HttpResponse
from .models import Grocery, Order, OrderItem, UserProfile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import GrocerySerializer, GroceryStockUpdateSerializer


# Create your views here.
def get_grocery_data(request):

    my_data = Grocery.objects.all()  # for all the records
    # one_data = userdetails.objects.get(pk=1) # 1 will return the first item change it depending on the data you want
    context = {
        "my_data": my_data,
    }

    return render(request, "get_grocery_data.html", context)


def get_order_data(request):

    my_data = Order.objects.all()  # for all the records
    # one_data = userdetails.objects.get(pk=1) # 1 will return the first item change it depending on the data you want
    context = {
        "my_data": my_data,
    }

    return render(request, "get_order_data.html", context)


def get_orderitem_data(request):

    my_data = OrderItem.objects.all()  # for all the records
    # one_data = userdetails.objects.get(pk=1) # 1 will return the first item change it depending on the data you want
    context = {
        "my_data": my_data,
    }

    return render(request, "get_orderitem_data.html", context)


def get_user_data(request):

    my_data = UserProfile.objects.all()  # for all the records
    # one_data = userdetails.objects.get(pk=1) # 1 will return the first item change it depending on the data you want
    context = {
        "my_data": my_data,
    }

    return render(request, "get_user_data.html", context)


@api_view(["GET"])
def get_grocery_details(request, gname):
    try:
        # Fetch the grocery data using the provided gname from the groceryStore_grocery table
        # grocery = Grocery.objects.using("groceryStore_grocery").get(gname=gname)
        grocery = Grocery.objects.get(gname=gname)
        # Serialize the grocery data
        serializer = GrocerySerializer(grocery)
        # Return the serialized data in the response
        return Response(serializer.data)
    except Grocery.DoesNotExist:
        # Return a 404 response if the grocery with the provided gname doesn't exist
        return Response({"message": "Grocery not found"}, status=404)


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
