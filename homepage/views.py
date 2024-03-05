from django.shortcuts import render

from .homepage import homepage_recipes_info


def homepage(request):
    return render(request, "homepage/homepage.html", {"recipes": homepage_recipes_info})
