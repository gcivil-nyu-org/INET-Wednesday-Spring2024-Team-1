import requests
import os

def recipe_info():
    # url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/"+str(id)+"/information"
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/798400/information"
    headers = {
	"X-RapidAPI-Key": os.environ.get('RAPID_API_KEY'),
	"X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }
    querystring = {"includeNutrition":"true"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()

recipe_information = recipe_info()