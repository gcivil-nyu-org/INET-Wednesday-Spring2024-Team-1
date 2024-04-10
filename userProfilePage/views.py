from django.shortcuts import render
import requests
from FoodSync.settings import BASE_API_URL

base_url = BASE_API_URL
# Create your views here.

def index(request):
    url = base_url + "get_order_data/"
    data = {'username': request.user.username}
    response = requests.post(url, data=data)
    orders = response.json()
    
    if orders is not None:
        for order in orders:
            items = order["orderitem_set"]
            for item in items:
                item["total"] = item["grocery"]["price"] * item["quantity"]
        return render(request, "userProfilePage/index.html", {"orders": orders})
    return render(request, "userProfilePage/index.html")
