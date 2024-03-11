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
    user_by_uid = CustomUser.objects.get(email=request.user.email)
    print(user_by_uid.preferences)
    if user_by_uid.preferences:
        return redirect("homepage")
    return render(request, "users/preferences.html")

def skip_preferences(request):
    return redirect("homepage")

def set_preferences(request):
    print("set_preferences")

    if request.method == 'POST':
        custom_user_instance = CustomUser.objects.get(email=request.user.email)
        form_data = request.POST
        phone_number = form_data['phone']
        address = form_data['address']
        diet = form_data['diet']
        cuisine_names = form_data.getlist('cuisine')
        allergy_names = form_data.getlist('allergies')
        height = form_data['height']
        weight = form_data['weight']
        target_weight = form_data['targetWeight']

        # Create UserPreferences instance
        user_preferences = UserPreferences.objects.create(
            user=custom_user_instance,
            phone_number=phone_number,
            address=address,
            diet=diet,
            height=height,
            weight=weight,
            target_weight=target_weight
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
        return render(request, 'preferences.html')