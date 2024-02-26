from django.shortcuts import render

from .recipe import recipe_information

def recipe(request):
    return render(request, 'recipe/recipe.html', {"recipe": recipe_information})