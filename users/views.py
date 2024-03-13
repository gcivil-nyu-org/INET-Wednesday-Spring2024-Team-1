from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import transaction
from django.template.response import TemplateResponse
from django.http import HttpResponse


import django

django.setup()

from users.models import CustomUser, UserPreferences, Cuisine, Allergy


def login(request):
    if request.user.is_authenticated:
        return redirect("homepage")
    return render(request, "users/login.html")


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
    if not request.user.is_authenticated:
        return redirect("/")
    return redirect("homepage")


def set_preferences(request):
    print("set_preferences")
    if not request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        print("POST")
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

        print("else")
        if (
            not phone_number
            or not address
            or not height
            or not weight
            or not target_weight
        ):
            return HttpResponse("Missing required fields", status=400)
        print("Creating UserPreferences instance")
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
