from django.shortcuts import render

import requests
import os


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
