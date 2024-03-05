from django.urls import path, include 
from . import views
from django.views.generic import TemplateView

from homepage.views import homepage

from django.contrib.auth.views import LogoutView

urlpatterns = [ 
   path('preferences/', TemplateView.as_view(template_name='users/preferences.html')),
   path("home", homepage, name="home"), 
#    path("logout",views.logout_view), 
   path('logout/', LogoutView.as_view(),name='logout'), 
   path('', views.login, name='login'), 
   path("accounts/",include("allauth.urls")), 
]