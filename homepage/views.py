import requests
import os

from django.shortcuts import render

from utils.homepage_utils import homepage_recipes

def homepage(request):
    if(request.session.get("homepage_recipes_info")):
        recipes_info = request.session.get("homepage_recipes_info")
        return render(request, "homepage/homepage.html", {"recipes": recipes_info})
    homepage_recipes(request)
    recipes_info = request.session.get("homepage_recipes_info")
    print("homepage view hello")
    return render(request, "homepage/homepage.html", {"recipes": recipes_info})
