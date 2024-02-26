from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def recipe(request):
    return render(request, 'recipe.html')