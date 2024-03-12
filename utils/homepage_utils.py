import requests
import os


def homepage_recipes(request):

    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/random"

    querystring = {"number": "16"}

    headers = {
        "X-RapidAPI-Key": os.environ.get("RAPID_API_KEY"),
        "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring)

    request.session["homepage_recipes_info"] = response.json()
