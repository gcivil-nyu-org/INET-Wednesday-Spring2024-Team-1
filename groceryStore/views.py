from django.shortcuts import render
from django.http import HttpResponse
from .models import Grocery, Order, OrderItem, UserProfile


# Create your views here.
def get_grocery_data(request):

    my_data = Grocery.objects.all()  # for all the records
    # one_data = userdetails.objects.get(pk=1) # 1 will return the first item change it depending on the data you want
    context = {
        "my_data": my_data,
        #'one_data':one_data,
    }

    return render(request, "get_grocery_data.html", context)


def get_order_data(request):

    my_data = Order.objects.all()  # for all the records
    # one_data = userdetails.objects.get(pk=1) # 1 will return the first item change it depending on the data you want
    context = {
        "my_data": my_data,
        #'one_data':one_data,
    }

    return render(request, "get_order_data.html", context)


def get_orderitem_data(request):

    my_data = OrderItem.objects.all()  # for all the records
    # one_data = userdetails.objects.get(pk=1) # 1 will return the first item change it depending on the data you want
    context = {
        "my_data": my_data,
        #'one_data':one_data,
    }

    return render(request, "get_orderitem_data.html", context)


def get_user_data(request):

    my_data = UserProfile.objects.all()  # for all the records
    # one_data = userdetails.objects.get(pk=1) # 1 will return the first item change it depending on the data you want
    context = {
        "my_data": my_data,
        #'one_data':one_data,
    }

    return render(request, "get_user_data.html", context)
