"""
URL configuration for FoodSync project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from FoodSync import views
from recipe import views as recipe_views
from django.contrib import admin

urlpatterns = [
    # path('', views.index, name='index'),
    path("recipe/", include("recipe.urls")),
    path("homepage/", include("homepage.urls")),
    path("groceryStore/", include("groceryStore.urls")),
    path("", include("users.urls")),
    path("admin/", admin.site.urls),
    path("addToCart/", recipe_views.add_to_cart, name="add_to_cart"),
    path("fetch-cart-data/", recipe_views.fetch_cart_data, name="fetch_cart_data"),
    path("update_cart/", recipe_views.update_cart, name="update_cart"),
    path(
        "check_session_variable/",
        recipe_views.check_session_variable,
        name="check_session_variable",
    ),
]
