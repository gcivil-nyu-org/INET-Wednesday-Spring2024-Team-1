from django.shortcuts import render
import requests
from FoodSync.settings import BASE_API_URL

base_url = BASE_API_URL
# Create your views here.

def index(request):
    name = request.session.get('username')
    url = base_url + "get_order_data/"
    response = requests.post(url, data={'username': name})
    orders = response.json()
    # print(response)
    for order in orders:
        items = order['orderitem_set']
        for item in items:
            item['total'] = item['grocery']['price'] * item['quantity']
    return render(request, 'userProfilePage/index.html', {'orders': orders})
