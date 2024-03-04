from django.urls import path, include 
from . import views 
from django.views.generic import TemplateView 
from django.contrib.auth.views import LogoutView

urlpatterns = [ 
               path("home/", TemplateView.as_view(template_name='users/home.html')), 
            #    path("logout",views.logout_view), 
               path('logout/', LogoutView.as_view(),name='logout'), 
               path('', views.login, name='login'), 
               path("accounts/",include("allauth.urls")), 
            ]