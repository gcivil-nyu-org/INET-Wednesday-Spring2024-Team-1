from django.shortcuts import render
import requests
import os
from django.http import JsonResponse
import json
from utils import groceryStore_utils

base_url = "http://127.0.0.1:8000/groceryStore/api/"


def recipe_info(request, recipe_id):
    print(recipe_id)
    url = (
        "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/"
        + str(recipe_id)
        + "/information"
    )
    # url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/798400/information"
    headers = {
        "X-RapidAPI-Key": os.environ.get("RAPID_API_KEY"),
        "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
    }
    querystring = {"includeNutrition": "true"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    return render(request, "recipe/recipe.html", {"recipe": response.json()})


def add_to_cart(request):
    if request.method == "POST":
        # Assuming you're receiving data in JSON format
        try:
            data = json.loads(request.body)
            cart_data = data["updated_data"]
            for item in cart_data:
                item_id = item["id"]
                temp = int(item["quantity"])
                if "price" not in item:
                    # Fetch grocery price and calculate item price
                    grocery_price = fetch_grocery_price(int(item_id), item["name"])
                    # if grocery_price is not None:
                    item["price"] = str(grocery_price * temp)
            request.session["cart_data"] = {"updated_data": cart_data}
            return JsonResponse({"success": True})
        except json.JSONDecodeError as e:
            # Handle JSON decoding error
            print("JSON Decode Error:", e)
            return JsonResponse({"success": False, "error": "Invalid JSON data"})
        except Exception as e:
            # Handle other exceptions
            print("Exception occurred:", e)
            return JsonResponse({"success": False, "error": "An error occurred"})
    return JsonResponse({"success": False, "error": "Invalid request method"})


def fetch_cart_data(request):
    # Retrieve cart data from session or database
    data = request.session.get("cart_data", [])
    cart_data = data["updated_data"]
    print("Cart data:", cart_data)
    # Iterate through cart_data and remove items with quantity <= 0
    cart_data = [item for item in cart_data if int(item["quantity"]) > 0]
    try:
        request_data = json.loads(request.body)
    except json.JSONDecodeError:
        # Handle case where request body is empty or not valid JSON
        request_data = {}
    cart_badge = request_data.get("cart_badge", False)
    if cart_badge:
        return JsonResponse({"cart_quantity": len(cart_data)})
    cart_html = "<table>"
    for item in cart_data:
        if int(item["quantity"]) <= 0:
            continue
        cart_html += '<tr id="tr_{}">'.format(item["id"])
        cart_html += "<td>{}</td>".format(item["name"])
        cart_html += '<td><button type="button" class="btn" onclick="decreaseQuantity({})">-</button></td>'.format(
            item["id"]
        )
        cart_html += '<td id="quantity_{}">{}</td>'.format(item["id"], item["quantity"])
        cart_html += '<td><button type="button" class="btn" onclick="increaseQuantity({})">+</button></td>'.format(
            item["id"]
        )
        cart_html += '<td id="price_{}">{}</td>'.format(item["id"], item["price"])
        cart_html += "</tr>"
    cart_html += "</table>"
    # Return cart data as JSON response
    return JsonResponse({"cart_items": cart_html, "cart_quantity": len(cart_data)})


def fetch_grocery_price(grocery_id, name):
    url = f"{base_url}groceries/{grocery_id}/"
    response = requests.get(url)
    if response.status_code == 200:
        grocery_details = response.json()
        return float(grocery_details["price"])
    else:
        # If grocery price is not found, add it to the database
        groceryStore_utils.grocery_addition(grocery_id, name)
        response = requests.get(url)
        if response.status_code == 200:
            grocery_details = response.json()
            return float(grocery_details["price"])
    return None


def update_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        item_id = data.get("itemId")
        change = data.get("change")
        session_data = request.session.get("cart_data", [])
        cart_data = session_data["updated_data"]
        for item in cart_data:
            if item["id"] == item_id:
                temp = int(item["quantity"])
                temp += int(change)
                if "price" not in item:
                    # Fetch grocery price and calculate item price
                    grocery_price = fetch_grocery_price(int(item_id), item["name"])
                    # if grocery_price is not None:
                    item["price"] = str(round(grocery_price * temp, 2))
                else:
                    # If item["price"] already exists, update it based on the new quantity
                    item["price"] = str(
                        round(fetch_grocery_price(int(item_id), item["name"]) * temp, 2)
                    )
                item["quantity"] = str(temp)
        request.session["cart_data"] = {"updated_data": cart_data}
        request.session.modified = True
        new_quantity = next(
            (item["quantity"] for item in cart_data if item["id"] == item_id), None
        )
        new_price = next(
            (item["price"] for item in cart_data if item["id"] == item_id), None
        )
        return JsonResponse({"newQuantity": new_quantity, "newPrice": new_price})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


def check_session_variable(request):
    if "cart_data" in request.session:
        exists = True
    else:
        exists = False
    return JsonResponse({"exists": exists})
