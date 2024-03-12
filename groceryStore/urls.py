from .views import (
    get_grocery_data,
    get_order_data,
    get_orderitem_data,
    get_user_data,
    get_grocery_details,
)
from django.urls import path, include


urlpatterns = [
    path("get_grocery_data/", get_grocery_data, name="get_grocery_data"),
    path("get_order_data/", get_order_data, name="get_order_data"),
    path("get_orderitem_data/", get_orderitem_data, name="get_orderitem_data"),
    path("get_user_data/", get_user_data, name="get_user_data"),
    path("api/groceries/<str:gname>/", get_grocery_details, name="get_grocery_details"),
]
