from django.shortcuts import render, redirect
import requests
from FoodSync.settings import BASE_API_URL
from users.models import CustomUser, UserCalorie
from django.utils import timezone
from django.forms.models import model_to_dict
from django.db.models import Sum
import json
from django.core.serializers.json import DjangoJSONEncoder

base_url = BASE_API_URL
# Create your views here.


def index(request):
    url = base_url + "get_order_data/"
    if request.user.is_authenticated:
        data = {"username": request.user.username}
        custom_user_instance = CustomUser.objects.get(email=request.user.email)
        calories_data = UserCalorie.objects.filter(user=custom_user_instance).values('date').annotate(total_calories=Sum('calories'))
        
        response = requests.post(url, data=data)
        orders = response.json()
        if orders is not None:
            for order in orders:
                items = order["orderitem_set"]
                for item in items:
                    item["total"] = float(item["grocery"]["price"]) * item["quantity"]
            calories_data_json = json.dumps(list(calories_data), cls=DjangoJSONEncoder)
            print(f'calories_data: {calories_data_json}')  # Debugging line
            response = render(request, "userProfilePage/index.html", {"orders": orders, "calories_data": calories_data_json})
        else:
            response = render(request, "userProfilePage/index.html")
    else:
        response = redirect("login")

    response["Cache-Control"] = "no-store"
    return response
