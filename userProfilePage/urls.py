from django.urls import path, include
from .views import index, callback

urlpatterns = [
    path('index/callback/', callback, name='callback'),
    path("", index, name="userProfilePage"),
]
