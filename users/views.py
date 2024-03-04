from django.shortcuts import render, redirect 
from django.contrib.auth import logout # Create your views here. 
def home(request):
    return render(request, "users/home.html") 

def logout_view(request):
    logout(request) # return redirect("/") 
    return redirect(r'^accounts/logout/$')
def login(request): 
    return render(request, "users/login.html")