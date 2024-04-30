from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import transaction
from django.template.response import TemplateResponse
from django.http import HttpResponse
from .forms import UserSignUpForm
from django.urls import reverse
import django
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from .signals import user_signed_up
from django.contrib.auth import authenticate, logout, login
from .models import CartData, UserCalorie
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

django.setup()

from users.models import CustomUser, UserPreferences, Cuisine, Allergy


def login_redirect(request):
    if request.user.is_authenticated:
        return redirect("homepage")
    return render(request, "users/login.html")


def logout_view(request):
    cart_data = request.session.get("cart_data", None)
    print("Cart data from logout:", cart_data)

    if request.user.is_authenticated and cart_data is not None:
        custom_user = CustomUser.objects.get(email=request.user.email)
        CartData.objects.update_or_create(
            user=custom_user, defaults={"data": cart_data}
        )

    logout(request)

    return redirect("/")


def signup(request):
    if request.user.is_authenticated:
        return redirect("homepage")
    return render(request, "users/signup.html")


def user_signup(request):
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            hashed_password = make_password(password)
            try:
                User.objects.create(
                    username=username, email=email, password=hashed_password
                )
                data = {"username": username, "email": email}
                user_signed_up(data, request)
                user = authenticate(request, username=username, password=password)
                login(request, user)
                return redirect(
                    "homepage"
                )  # Redirect to login page after successful signup
            except Exception as e:
                print(e)
                return TemplateResponse(
                    request,
                    "users/signup.html",
                    {"form": form, "error": "Error creating user"},
                )
    else:
        form = UserSignUpForm()
    return TemplateResponse(
        request, "users/signup.html", {"form": form, "error": "Error creating user"}
    )


def user_login(request):
    if request.method == "POST":
        form_data = request.POST
        username = form_data.get("username")
        password = form_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # user_logged_in(username, request)
            return redirect(
                reverse("homepage")
            )  # Replace 'dashboard' with the desired URL name
        else:
            # If authentication fails, display an error message
            error_message = "Invalid username or password."
            return render(request, "users/login.html", {"error_message": error_message})

    return TemplateResponse(request, "users/login.html")


PREFERENCES_TEMPLATE = "users/preferences.html"


def preferences(request):
    if not request.user.is_authenticated:
        return redirect("/")
    try:
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
            response = TemplateResponse(
                request, PREFERENCES_TEMPLATE, {"preferences": preferences}
            )
        else:
            response = TemplateResponse(
                request, "users/preferences.html", {"preferences": None}
            )
    except CustomUser.DoesNotExist:
        return redirect("/")

    response["Cache-Control"] = "no-store"
    return response

    return HttpResponse("Something went wrong.", status=500)


def skip_preferences(request):
    if not request.user.is_authenticated:
        return redirect("/")
    return redirect("homepage")


def set_preferences(request):
    if not request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        custom_user_instance = CustomUser.objects.get(email=request.user.email)
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


@csrf_exempt
def track_calories(request):
    if not request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        custom_user_instance = CustomUser.objects.get(email=request.user.email)
        amount = request.POST.get("amount")
        recipe_id = request.POST.get("recipe_id")
        existing_cals = UserCalorie.objects.filter(user=custom_user_instance, date=timezone.now().date(), recipeId=recipe_id).first()

        if existing_cals:
            # If a record for today exists, add the incoming calories to it
            existing_cals.calories += float(amount)
            existing_cals.save()
        else:
            # If no record for today exists, create a new one
            UserCalorie.objects.create(user=custom_user_instance, date=timezone.now().date(), calories=float(amount), recipeId = recipe_id)

        return JsonResponse({'status': 'success', 'message': 'Calories tracked successfully'})
    

# def get_calories(request):
#     if not request.user.is_authenticated:
#         return redirect("/")
#     if request.method == "GET":
#         custom_user_instance = CustomUser.objects.get(email=request.user.email)
#         user_calories = UserCalorie.objects.filter(user=custom_user_instance, date=timezone.now().date())
#         total_calories = sum([cal.calories for cal in user_calories])
#         return JsonResponse({'status': 'success', 'total_calories': total_calories})
#     return JsonResponse({'status': 'error', 'message': 'Invalid request method'})