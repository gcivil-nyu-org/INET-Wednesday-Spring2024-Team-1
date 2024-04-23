from django.shortcuts import render, redirect
import requests
from FoodSync.settings import BASE_API_URL
from django.http import JsonResponse
from users.models import CustomUser
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import json
import datetime
import traceback
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from dateutil.relativedelta import relativedelta
from django.http import HttpResponse
base_url = BASE_API_URL
# Create your views here.

# def index(request):
#     url = base_url + "get_order_data/"
#     data = {"username": request.user.username}
#     response = requests.post(url, data=data)
#     orders = response.json()
#     if orders is not None:
#         for order in orders:
#             items = order["orderitem_set"]
#             for item in items:
#                 item["total"] = item["grocery"]["price"] * item["quantity"]
#         return render(request, "userProfilePage/index.html", {"orders": orders})
#     return render(request, "userProfilePage/index.html")



def index(request):
    print(request.user.email)
    custom_user_instance = CustomUser.objects.get(email=request.user.email)
    if custom_user_instance.credentials:
        credentials_dict = json.loads(custom_user_instance.credentials)
        if 'refresh_token' not in credentials_dict:
            credentials_dict['refresh_token'] = ''
        print(credentials_dict)
        credentials = Credentials.from_authorized_user_info(credentials_dict)
        if credentials.expired:
            try:
                credentials.refresh(request)
            except Exception as e:
                print(e)
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
        print(e)
    calories_data = []
    labels = []
    current_date = datetime.datetime.utcnow()
    for i in range(30):
        date = (current_date - relativedelta(days=i)).strftime('%Y-%m-%d')
        calories = 0
        try:
            calories = data['bucket'][i]['dataset'][0]['point'][0]['value'][0]['fpVal']
        except Exception as e:
            print(e)
        calories_data.append((date, calories))
    # Prepare data for the template
    labels = [item[0] for item in reversed(calories_data)]  
    calorie_values = [item[1] for item in calories_data]

          
    

    # url = base_url + "get_order_data/"
    # data = {"username": request.user.username}
    # response = requests.post(url, data=data)
    # orders = response.json()
    # if orders is not None:
    #     for order in orders:
    #         items = order["orderitem_set"]
    #         for item in items:
    #             item["total"] = item["grocery"]["price"] * item["quantity"]
    #     return render(request, "userProfilePage/index.html", {"orders": orders, 'labels': labels, 'calorie_values': calorie_values})
    return render(request, "userProfilePage/index.html", {'labels': labels, 'calorie_values': calorie_values})

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
    flow.redirect_uri = 'https://localhost:8000/userProfilePage/index/callback/'
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
    flow.redirect_uri = 'https://localhost:8000/userProfilePage/index/callback/'
    try:
        flow.fetch_token(authorization_response=request.build_absolute_uri())
    except Exception as e:
        return HttpResponse(f'Error fetching token: {e}')

    custom_user_instance = CustomUser.objects.get(email=request.user.email)
    custom_user_instance.credentials = flow.credentials.to_json()
    custom_user_instance.save()
    return redirect("userProfilePage")
    
   
