from .views import (
    get_order_data,
    get_grocery_details,
    update_grocery_stock,
    place_order,
    clear_cart_data,
)
from django.urls import path, include


urlpatterns = [
    path("api/get_order_data/", get_order_data, name="get_order_data"),
    path(
        "api/groceries/<int:grocery_id>/",
        get_grocery_details,
        name="get_grocery_details",
    ),
    path("api/place_order/", place_order, name="place_order"),
    path(
        "update_stock/<str:gname>/", update_grocery_stock, name="update_grocery_stock"
    ),
    path("api/clear_cart_data/", clear_cart_data, name="clear_cart_data"),
]
