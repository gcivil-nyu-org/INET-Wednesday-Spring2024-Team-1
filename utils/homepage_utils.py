import requests
import os

from users import models

API_HOST = "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
base_url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"


def homepage_recipes(request):
    email = None
    if hasattr(request.user, "email"):
        email = request.user.email
    if email:
        user = models.CustomUser.objects.get(email=email)
        if user.preferences:
            user_preferences = models.UserPreferences.objects.get(user=user)
            diet = user_preferences.diet
            cuisines = user_preferences.cuisines.values_list("name", flat=True)
            allergies = user_preferences.allergies.values_list("name", flat=True)
            cuisines = ",".join([cuisine.lower() for cuisine in cuisines])
            allergies = ",".join([allergy.lower() for allergy in allergies])
            url = base_url + "recipes/complexSearch"

            querystring = {
                "diet": diet,
                "cuisine": cuisines,
                "intolerances": allergies,
                "number": "16",
            }

            headers = {
                "X-RapidAPI-Key": os.environ.get("RAPID_API_KEY"),
                "X-RapidAPI-Host": API_HOST,
            }

            response = requests.get(url, headers=headers, params=querystring)

            results = response.json()["results"]

            recipes = {"recipes": results}

            request.session["homepage_recipes_info"] = recipes

        else:
            url = base_url + "recipes/random"

            querystring = {"number": "16"}

            headers = {
                "X-RapidAPI-Key": os.environ.get("RAPID_API_KEY"),
                "X-RapidAPI-Host": API_HOST,
            }

            response = requests.get(url, headers=headers, params=querystring)

            request.session["homepage_recipes_info"] = response.json()
    else:
        url = base_url + "recipes/random"

        querystring = {"number": "16"}

        headers = {
            "X-RapidAPI-Key": os.environ.get("RAPID_API_KEY"),
            "X-RapidAPI-Host": API_HOST,
        }

        response = requests.get(url, headers=headers, params=querystring)

        request.session["homepage_recipes_info"] = response.json()
