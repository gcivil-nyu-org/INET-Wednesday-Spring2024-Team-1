from django.shortcuts import render
import requests

base_url = "http://127.0.0.1:8000/groceryStore/api/"
# Create your views here.

def index(request):
    user = request.user
    if user.is_authenticated:
        if user.socialaccount_set.all():
            # User has social accounts, get the name from the first one
            name = user.socialaccount_set.all()[0].extra_data['name']
        else:
            # User does not have social accounts, use the username
            name = user.username
    request.session['username'] = name
    url = base_url + "get_order_data/"
    response = requests.post(url, data={'username': name})
    orders = response.json()
    print(orders)
    for order in orders:
        items = order['orderitem_set']
        for item in items:
            item['total'] = item['grocery']['price'] * item['quantity']
            # item.total = item.grocery.price * item.quantity
    return render(request, 'userProfilePage/index.html', {'orders': orders})
