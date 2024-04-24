from django.shortcuts import render, redirect
import requests
from FoodSync.settings import BASE_API_URL

base_url = BASE_API_URL
# Create your views here.


def index(request):
    url = base_url + "get_order_data/"
    if request.user.is_authenticated:
        data = {"username": request.user.username}
        # if data["username"]:
        response = requests.post(url, data=data)
        orders = response.json()
        if orders is not None:
            for order in orders:
                items = order["orderitem_set"]
                for item in items:
                    item["total"] = float(item["grocery"]["price"]) * item["quantity"]
            response = render(request, "userProfilePage/index.html", {"orders": orders})
        else:
            response = render(request, "userProfilePage/index.html")
    else:
        response = redirect("login")

    response["Cache-Control"] = "no-store"
    return response
