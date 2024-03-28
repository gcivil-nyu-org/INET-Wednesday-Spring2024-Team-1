from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import transaction
from django.template.response import TemplateResponse
from django.http import HttpResponse
from .forms import UserSignUpForm
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse
import django
from django.contrib.auth.hashers import make_password
from .signals import user_signed_up, user_logged_in
from django.contrib.auth import authenticate, logout, login
from django.urls import reverse_lazy

django.setup()

from users.models import CustomUser, UserPreferences, Cuisine, Allergy

def login_redirect(request):
    if request.user.is_authenticated:
        return redirect("homepage")
    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return redirect("/")

def signup(request):
    if request.user.is_authenticated:
        return redirect("homepage")
    return render(request, "users/signup.html")

def user_signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            hashed_password = make_password(password)
            try:
                new_user = User.objects.create(username=username, email=email, password=hashed_password)
                # request.session["email"] = email
                # Call any additional function after signup
                data = {
                    "username": username, "email": email
                }
                user_signed_up(data, request)
                user = authenticate(request, username=username, password=password)
                login(request, user)
                return redirect('homepage')  # Redirect to login page after successful signup
            except Exception as e:
                # return render(request, 'signup.html', {'form': form, 'error': 'Error creating user'})
                return TemplateResponse(
                    request, "users/signup.html", {'form': form, 'error': 'Error creating user'}
                )
    else:
        form = UserSignUpForm()
    return TemplateResponse(
        request, "users/signup.html", {'form': form, 'error': 'Error creating user'}
    )

def user_login(request):
    if request.method == 'POST':
        form_data = request.POST
        username = form_data.get('username')
        password = form_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # user_logged_in(username, request)
            return redirect(reverse("homepage"))  # Replace 'dashboard' with the desired URL name
        else:
            # If authentication fails, display an error message
            error_message = "Invalid username or password."
            return render(request, 'users/login.html', {'error_message': error_message})

    return TemplateResponse(
        request, "users/login.html"
    )

def preferences(request):
    if not request.user.is_authenticated:
        return redirect("/")
    try:
        # if request.user.is_authenticated:
        #     email = request.user.email
        # else:
        #     email = request.session.get("customUserLoggedIn")["email"]
        custom_user_instance = CustomUser.objects.get(email=request.user.email)
        if custom_user_instance.preferences:
            user_preferences = UserPreferences.objects.get(user=custom_user_instance)
            cuisines = user_preferences.cuisines.values_list("name", flat=True)
            allergies = user_preferences.allergies.values_list("name", flat=True)
            preferences = {
                "phone_number": user_preferences.phone_number,
                "address": user_preferences.address,
                "diet": user_preferences.diet,
                "cuisines": list(cuisines),
                "allergies": list(allergies),
                "height": user_preferences.height,
                "weight": user_preferences.weight,
                "target_weight": user_preferences.target_weight,
            }
            return TemplateResponse(
                request, "users/preferences.html", {"preferences": preferences}
            )
        else:
            return TemplateResponse(
                request, "users/preferences.html", {"preferences": None}
            )
    except CustomUser.DoesNotExist:
        return redirect("/")

    return HttpResponse("Something went wrong.", status=500)


def skip_preferences(request):
    if not request.user.is_authenticated and request.session.get("customUserLoggedIn") is False:
        return redirect("/")
    return redirect("homepage")


def set_preferences(request):
    if not request.user.is_authenticated and request.session.get("customUserLoggedIn") is False:
        return redirect("/")
    if request.method == "POST":
        if request.user.is_authenticated:
            email = request.user.email
        else:
            email = request.session.get("customUserLoggedIn")["email"]
        custom_user_instance = CustomUser.objects.get(email=email)
        form_data = request.POST
        phone_number = form_data.get("phone")
        address = form_data.get("address")
        diet = form_data.get("diet")
        cuisine_names = form_data.getlist("cuisine")
        allergy_names = form_data.getlist("allergies")
        height = form_data.get("height")
        weight = form_data.get("weight")
        target_weight = form_data.get("targetWeight")

        if custom_user_instance.preferences:
            user_preferences = UserPreferences.objects.get(user=custom_user_instance)
            user_preferences.phone_number = phone_number
            user_preferences.address = address
            user_preferences.diet = diet
            user_preferences.cuisines.clear()  # Clear existing cuisines
            user_preferences.allergies.clear()  # Clear existing allergies
            # Add selected cuisines and allergies
            cuisines = Cuisine.objects.filter(name__in=cuisine_names)
            # Retrieve Allergy objects for each allergy name
            allergies = Allergy.objects.filter(name__in=allergy_names)
            # Add cuisines (assuming cuisines is a ManyToManyField)
            user_preferences.cuisines.add(*cuisines)
            user_preferences.allergies.add(*allergies)
            user_preferences.height = height
            user_preferences.weight = weight
            user_preferences.target_weight = target_weight
            user_preferences.save()
            request.session["preferences_updated"] = True
            return redirect("homepage")

        if (
            not phone_number
            or not address
            or not height
            or not weight
            or not target_weight
        ):
            return HttpResponse("Missing required fields", status=400)
        user_preferences = UserPreferences.objects.create(
            user=custom_user_instance,
            phone_number=phone_number,
            address=address,
            diet=diet,
            height=height,
            weight=weight,
            target_weight=target_weight,
        )
        cuisines = Cuisine.objects.filter(name__in=cuisine_names)
        # Retrieve Allergy objects for each allergy name
        allergies = Allergy.objects.filter(name__in=allergy_names)
        try:
            with transaction.atomic():
                # Create UserPreferences instance
                # Add cuisines (assuming cuisines is a ManyToManyField)
                user_preferences.cuisines.add(*cuisines)
                user_preferences.allergies.add(*allergies)
                user_preferences.save()
                custom_user_instance.preferences = True
                custom_user_instance.save()
                request.session["check_user_preferences"] = True
                request.session["preferences_updated"] = True
                request.session["preferences_set"] = True
        except Exception as e:
            print(e)
            return HttpResponse("Something went wrong", status=400)
        return redirect("homepage")
    else:
        return TemplateResponse(
            request, "users/preferences.html", {"preferences_set_error": None}
        )
