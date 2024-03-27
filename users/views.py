from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import transaction
from django.template.response import TemplateResponse
from django.http import HttpResponse
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import datetime
import traceback
from dateutil.relativedelta import relativedelta
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import django
import json
from google.oauth2.credentials import Credentials
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

def show_profile(request):
    if not request.user.is_authenticated:
        return redirect("/")
    custom_user_instance = CustomUser.objects.get(email=request.user.email)
    credentials = None
    if custom_user_instance.credentials:
        credentials_dict = json.loads(custom_user_instance.credentials)
        if 'refresh_token' not in credentials_dict:
            credentials_dict['refresh_token'] = ''
        print(credentials_dict)
        credentials = Credentials.from_authorized_user_info(credentials_dict)
        if credentials.expired:
            try:
                credentials.refresh(Request())
            except Exception as e:
                return auth(request)
    else:
        return auth(request)
    service = build('fitness', 'v1', credentials=credentials)
    current_date = datetime.datetime.utcnow()

    end_time = int(datetime.datetime.utcnow().timestamp() * 1000)
    start_time = end_time - (30 * 24 * 60 * 60 * 1000)  

    try:
        data = service.users().dataset().aggregate(
            userId='me',
            body={
                "aggregateBy": [{"dataTypeName": "com.google.calories.expended", "dataSourceId": 'derived:com.google.calories.expended:com.google.android.gms:merge_calories_expended'}],
                "bucketByTime": {"durationMillis": 24 * 60 * 60 * 1000},  
                "startTimeMillis": start_time,
                "endTimeMillis": end_time,
            }
        ).execute()
    except Exception as e:
        return HttpResponse(f'Error fetching fitness data or there are no data in your google fit: {e}')
    calories_data = []
    current_date = datetime.datetime.utcnow()
    for i in range(30):
        date = (current_date - relativedelta(days=i)).strftime('%Y-%m-%d')
        calories = 0
        try:
            calories = data['bucket'][i]['dataset'][0]['point'][0]['value'][0]['fpVal']
        except (KeyError, IndexError):
            print('not exist')
        calories_data.append((date, calories))
    # Prepare data for the template
    labels = [item[0] for item in reversed(calories_data)]  
    calorie_values = [item[1] for item in calories_data]  
    print(labels)
    print(calorie_values)
    context = {
        'labels': labels,
        'calorie_values': calorie_values,
    }

    return render(request, 'users/profile.html', context)

def auth(request):
    flow = InstalledAppFlow.from_client_config(
    client_config = {
        "web":{
            "client_id":os.environ.get("google_client_id"),
            "auth_uri":"https://accounts.google.com/o/oauth2/auth",
            "token_uri":"https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
            "client_secret":os.environ.get("google_secret"),
            }},
    scopes=['https://www.googleapis.com/auth/fitness.activity.read']
    )
    flow.redirect_uri = 'https://localhost:8000/profile/callback/'
    authorization_url, _ = flow.authorization_url(access_type='offline')
    request.session['authorization_url'] = authorization_url
    print(authorization_url)
    return redirect(authorization_url)

def callback(request):
    authorization_url = request.session.get('authorization_url')
    if not authorization_url:
        return HttpResponse('Authorization URL not found in session. Please try again.')
    flow = InstalledAppFlow.from_client_config(
    client_config = {
            "web":{
                "client_id":os.environ.get("google_client_id"),
                "auth_uri":"https://accounts.google.com/o/oauth2/auth",
                "token_uri":"https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
                "client_secret":os.environ.get("google_secret"),
                }},
    scopes=['https://www.googleapis.com/auth/fitness.activity.read']
    )
    flow.redirect_uri = 'https://localhost:8000/profile/callback/'
    try:
        flow.fetch_token(authorization_response=request.build_absolute_uri())
    except Exception as e:
        return HttpResponse(f'Error fetching token: {e}')

    custom_user_instance = CustomUser.objects.get(email=request.user.email)
    custom_user_instance.credentials = flow.credentials.to_json()
    custom_user_instance.save()
    return redirect("showProfile")
    
   