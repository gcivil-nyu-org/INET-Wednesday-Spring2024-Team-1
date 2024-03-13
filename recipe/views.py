from django.shortcuts import render
import requests
import os
from django.http import JsonResponse
import json


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
            cart_data = json.loads(request.body)
            request.session["cart_data"] = cart_data
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
        cart_html += "</tr>"
    cart_html += "</table>"
    # Return cart data as JSON response
    return JsonResponse({"cart_items": cart_html})


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
                item["quantity"] = str(temp)
                break
        request.session["cart_data"] = {"updated_data": cart_data}
        request.session.modified = True
        new_quantity = next(
            (item["quantity"] for item in cart_data if item["id"] == item_id), None
        )
        return JsonResponse({"newQuantity": new_quantity})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


def check_session_variable(request):
    if "cart_data" in request.session:
        exists = True
    else:
        exists = False
    return JsonResponse({"exists": exists})
