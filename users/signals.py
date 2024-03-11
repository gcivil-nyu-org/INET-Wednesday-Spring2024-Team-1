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

    # print(auth_user.email)

    # Check if the corresponding CustomUser already exists
    try:
        custom_user = CustomUser.objects.get(email=auth_user.email)
    except CustomUser.DoesNotExist:
        # If CustomUser does not exist, create a new one
        custom_user = CustomUser(email=auth_user.email)

    # Update CustomUser fields with auth_user data
        custom_user.username = auth_user.username
        custom_user.preferences = "False"
        custom_user.save()
