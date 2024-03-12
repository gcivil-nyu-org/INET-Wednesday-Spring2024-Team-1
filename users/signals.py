# Import necessary modules and signals
from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import CustomUser  # Replace 'your_app' with your app name


# Define a receiver function for the user_logged_in signal
@receiver(user_logged_in)
def update_custom_user(sender, user, request, **kwargs):
    print("update_custom_user", user.email)
    # Retrieve the user data from the auth_user table
    auth_user = User.objects.get(email=user.email)
    try:
        custom_user = CustomUser.objects.get(email=auth_user.email)
    except CustomUser.DoesNotExist:
        custom_user = CustomUser(email=auth_user.email)
        custom_user.username = auth_user.username
        custom_user.preferences = "False"
        custom_user.save()
