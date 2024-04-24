from django.urls import path, include
from . import views
from django.views.generic import TemplateView

from homepage.views import homepage

from django.contrib.auth.views import LogoutView

urlpatterns = [
    # path("preferences/", TemplateView.as_view(template_name="users/preferences.html")),
    path("preferences/", views.preferences, name="preferences"),
    path("homepage", homepage, name="homepage"),
    #    path("",views.logout_view),
    path("logout/", views.logout_view, name="logout"),
    path("", views.login_redirect, name="login"),
    path("signup/", views.signup, name="signup"),
    path("userSignup/", views.user_signup, name="userSignup"),
    path("userLogin/", views.user_login, name="userLogin"),
    path("accounts/", include("allauth.urls")),
    path("setPreferences/", views.set_preferences, name="setPreferences"),
    path("skipPreferences/", views.skip_preferences, name="skipPreferences"),
]
