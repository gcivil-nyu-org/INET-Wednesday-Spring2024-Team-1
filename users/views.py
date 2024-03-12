from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import transaction

import django

django.setup()

from users.models import CustomUser, UserPreferences, Cuisine, Allergy


def login(request):
    if request.user.is_authenticated:
        return redirect("homepage")
    return render(request, "users/login.html")


def preferences(request):
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
        return render(request, "users/preferences.html", {"preferences": preferences})
    return render(request, "users/preferences.html")


def skip_preferences(request):
    return redirect("homepage")


def set_preferences(request):
    print("set_preferences")

    if request.method == "POST":
        custom_user_instance = CustomUser.objects.get(email=request.user.email)
        form_data = request.POST
        phone_number = form_data["phone"]
        address = form_data["address"]
        diet = form_data["diet"]
        cuisine_names = form_data.getlist("cuisine")
        allergy_names = form_data.getlist("allergies")
        height = form_data["height"]
        weight = form_data["weight"]
        target_weight = form_data["targetWeight"]

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
            request.session['preferences_updated'] = True
            return redirect("homepage")

        # Create UserPreferences instance
        user_preferences = UserPreferences.objects.create(
            user=custom_user_instance,
            phone_number=phone_number,
            address=address,
            diet=diet,
            height=height,
            weight=weight,
            target_weight=target_weight,
        )
        print(form_data)

        cuisines = Cuisine.objects.filter(name__in=cuisine_names)
        # Retrieve Allergy objects for each allergy name
        allergies = Allergy.objects.filter(name__in=allergy_names)
        # Add cuisines (assuming cuisines is a ManyToManyField)

        try:
            with transaction.atomic():
                user_preferences.cuisines.add(*cuisines)
                user_preferences.allergies.add(*allergies)
                user_preferences.save()
                custom_user_instance.preferences = True
                custom_user_instance.save()
        except Exception as e:
            # Handle exception
            print("Error occurred:", e)
        return redirect("homepage")
    else:
        return render(request, "preferences.html")
