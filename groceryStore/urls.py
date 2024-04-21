from .views import (
    get_grocery_data,
    get_order_data,
    get_orderitem_data,
    get_user_data,
    get_grocery_details,
    update_grocery_stock,
<<<<<<< HEAD
=======
    place_order,
    clear_cart_data,
>>>>>>> develop
)
from django.urls import path, include


urlpatterns = [
    path("get_grocery_data/", get_grocery_data, name="get_grocery_data"),
    path("get_orderitem_data/", get_orderitem_data, name="get_orderitem_data"),
    path("get_user_data/", get_user_data, name="get_user_data"),
<<<<<<< HEAD
    path("api/groceries/<str:gname>/", get_grocery_details, name="get_grocery_details"),
    path(
        "update_stock/<str:gname>/", update_grocery_stock, name="update_grocery_stock"
    ),
=======
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
>>>>>>> develop
]
