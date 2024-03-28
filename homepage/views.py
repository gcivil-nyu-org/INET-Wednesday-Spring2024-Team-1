import requests
import os

from django.shortcuts import render

from utils.homepage_utils import homepage_recipes

def homepage(request):
    preferences_updated = request.session.pop("preferences_updated", False)
    check_user_preferences = request.session.get("check_user_preferences")
    # Check if preferences have been updated
    if preferences_updated:
        homepage_recipes(request)
    if request.session.get("homepage_recipes_info"):
        recipes_info = request.session.get("homepage_recipes_info")
        return render(request, "homepage/homepage.html", {"recipes": recipes_info})
    homepage_recipes(request)
    recipes_info = request.session.get("homepage_recipes_info")
    return render(
        request,
        "homepage/homepage.html",
        {"recipes": recipes_info, "check_user_preferences": check_user_preferences},
    )
