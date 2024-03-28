# Import necessary modules and signals
from allauth.account.signals import user_logged_in as allauth_signal
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import CustomUser, UserPreferences
from django.utils import timezone


# Define a receiver function for the user_logged_in signal
@receiver([allauth_signal, user_logged_in])
def update_custom_user(sender, user, request, **kwargs):
    # Retrieve the user data from the auth_user table
    auth_user = User.objects.get(username=user.username)
    print(auth_user)
    try:
        custom_user = CustomUser.objects.get(username=auth_user.username)
        custom_user.last_login = timezone.now()
        custom_user.save()
        request.session["check_user_preferences"] = custom_user.preferences

    except CustomUser.DoesNotExist:
        custom_user = CustomUser(email=auth_user.email)
        custom_user.username = auth_user.username
        custom_user.preferences = "False"
        custom_user.last_login = timezone.now()
        custom_user.save()


def user_signed_up(data, request):
    CustomUser.objects.create(
        username=data["username"],
        email=data["email"],
        preferences=False,
        last_login=timezone.now()
    )
    request.session["check_user_preferences"] = "False"
