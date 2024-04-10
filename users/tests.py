import datetime
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.db import models
from .models import CustomUser, UserPreferences, Cuisine, Allergy
from django.utils import timezone
from .views import preferences, login_redirect, set_preferences, skip_preferences
from django.dispatch import Signal
from .signals import update_custom_user, user_logged_in, user_signed_up
from .forms import UserSignUpForm
from unittest.mock import patch
from django.utils import timezone
from freezegun import freeze_time
from unittest.mock import MagicMock
from rest_framework.test import force_authenticate

class UserPreferencesTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.factory = RequestFactory()
        User.objects.create_user(
            username="testuser", email="test@example.com", last_login=timezone.now()
        )
        self.customUser = CustomUser.objects.create(
            username="testuser",
            email="test@example.com",
            preferences="True",
            last_login=timezone.now(),
        )
        self.client = Client()

    def test_authenticated_user_redirect_to_homepage(self):
        request = self.factory.get(reverse("login"))
        request.user = self.customUser
        request.user.is_authenticated = lambda: True
        response = login_redirect(request)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, reverse("homepage"))

    def test_unauthenticated_user_render_login_page(self):
        request = self.factory.get(reverse("login"))
        request.user = AnonymousUser()
        response = login_redirect(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Continue with Google", response.content.decode())

    def test_create_custom_user(self):
        # Create a CustomUser object
        CustomUser.objects.create(
            username="test",
            email="test@test.com",
            preferences=True,  # Set preferences to True for demonstration
            last_login=timezone.make_aware(
                timezone.datetime(2022, 1, 1)
            ),  # Set last_login to a specific datetime for demonstration
        )

        # Retrieve the created CustomUser object from the database
        retrieved_custom_user = CustomUser.objects.get(email="test@test.com")

        # Verify that the retrieved CustomUser object matches the expected values
        self.assertEqual(retrieved_custom_user.username, "test")
        self.assertEqual(retrieved_custom_user.email, "test@test.com")
        self.assertEqual(retrieved_custom_user.preferences, True)
        self.assertEqual(
            retrieved_custom_user.last_login,
            timezone.make_aware(timezone.datetime(2022, 1, 1)),
        )

    def test_create_user_preferences(self):
        # Create user preferences
        UserPreferences.objects.create(
            user=self.customUser,
            phone_number="1234567890",
            address="Test Address",
            diet="vegetarian",
            height=170,
            weight=150,
            target_weight=140,
        )

        self.cuisine1 = Cuisine.objects.create(name="Chinese")
        self.cuisine2 = Cuisine.objects.create(name="Indian")
        self.allergy1 = Allergy.objects.create(name="Dairy")
        self.allergy2 = Allergy.objects.create(name="Nuts")

        # Retrieve the created user preferences
        user_preferences = UserPreferences.objects.get(user=self.customUser)
        user_preferences.cuisines.add(self.cuisine1)
        user_preferences.allergies.add(self.allergy1)

        # Check if the created user preferences match the provided data
        self.assertEqual(user_preferences.phone_number, "1234567890")
        self.assertEqual(user_preferences.address, "Test Address")
        self.assertEqual(user_preferences.diet, "vegetarian")
        self.assertEqual(user_preferences.height, 170)
        self.assertEqual(user_preferences.weight, 150)
        self.assertEqual(user_preferences.target_weight, 140)

        # Check if cuisines and allergies are properly associated
        self.assertIn(self.cuisine1, user_preferences.cuisines.all())
        self.assertNotIn(self.cuisine2, user_preferences.cuisines.all())
        self.assertIn(self.allergy1, user_preferences.allergies.all())
        self.assertNotIn(self.allergy2, user_preferences.allergies.all())

    def test_update_user_preferences(self):
        # Create user preferences
        user_preferences = UserPreferences.objects.create(
            user=self.customUser,
            phone_number="1234567890",
            address="Test Address",
            diet="vegetarian",
            height=170,
            weight=150,
            target_weight=140,
        )

        # Update user preferences
        user_preferences.diet = "vegan"
        user_preferences.save()

        # Retrieve the updated user preferences
        updated_preferences = UserPreferences.objects.get(user=self.customUser)

        # Check if the diet field is updated
        self.assertEqual(updated_preferences.diet, "vegan")

    def test_delete_user_preferences(self):
        user_preferences = UserPreferences.objects.create(
            user=self.customUser,
            phone_number="1234567890",
            address="Test Address",
            diet="vegetarian",
            height=170,
            weight=150,
            target_weight=140,
        )

        # Delete user preferences
        user_preferences.delete()

        # Ensure the preferences are deleted
        with self.assertRaises(UserPreferences.DoesNotExist):
            UserPreferences.objects.get(user=self.customUser)

    def test_set_preferences_valid_data_anonymous(self):
        data = {
            "phone": "1234567890",
            "address": "Test Address",
            "diet": "vegetarian",
            "cuisine": ["Indian", "Italian"],
            "allergies": ["Dairy", "Nuts"],
            "height": "170",
            "weight": "150",
            "targetWeight": "140",
        }
        request = self.factory.get(reverse("setPreferences"))
        request.user = AnonymousUser()
        request.data = data
        response = set_preferences(request)
        self.assertEqual(
            response.status_code, 302
        )  # Redirects to login page for anonymous users

    def test_set_preferences_anonymous(self):
        request = self.factory.get(reverse("setPreferences"))
        request.user = AnonymousUser()
        response = set_preferences(request)
        self.assertEqual(response.status_code, 302)


    def test_set_preferences_valid_data_authenticated_set(self):
        data = {
            "phone": "1234567890",
            "address": "Test Address",
            "diet": "vegetarian",
            "cuisine": ["Indian", "Italian"],
            "allergies": ["Dairy", "Nuts"],
            "height": "170",
            "weight": "150",
            "targetWeight": "140",
        }

        fq = RequestFactory()
        custom_user = CustomUser.objects.create(
            username="test", email="test@test.com", preferences="False"
        )
        request = fq.post(reverse("setPreferences"), data=data)

        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()

        request.user = custom_user
        force_authenticate(request, user=custom_user)

        request.user.is_authenticated = lambda: True
        response = set_preferences(request)
        self.assertTrue(request.session["preferences_updated"])
        self.assertTrue(request.session['preferences_set'])
        self.assertTrue(request.session["check_user_preferences"])
        # Check if the response status code is 302
        self.assertEqual(response.status_code, 302)

    # def test_set_preferences_valid_data_authenticated_update(self):
    #     data = {
    #         'cuisine': ['Indian'],
    #         'allergies': ['Dairy']
    #     }
    #     fq = RequestFactory()
    #     custom_user = CustomUser.objects.create(
    #         username="test", email="test@test.com", preferences="True"
    #     )
    #     request = fq.post(reverse("setPreferences"), data=data)

    #     middleware = SessionMiddleware(lambda req: None)
    #     middleware.process_request(request)
    #     request.session.save()

    #     request.user = custom_user
    #     force_authenticate(request, user=custom_user)

    #     request.user.is_authenticated = lambda: True

    #     response = set_preferences(request)
    #     self.assertTrue(request.session['preferences_updated'])
    #     self.assertEqual(response.status_code, 302)

    def test_set_preferences_invalid_data_authenticated_set(self):
        data = {
            "address": "Test Address",
            "diet": "vegetarian",
            "cuisine": ["Indian", "Italian"],
            "allergies": ["Dairy", "Nuts"],
            "height": "170",
            "weight": "150",
            "targetWeight": "140",
        }
        custom_user = CustomUser.objects.create(
            username="test", email="test@test.com", preferences="False"
        )
        custom_user_instance = CustomUser.objects.get(email=custom_user.email)
        request = self.factory.post(reverse("setPreferences"))
        request.user = custom_user_instance
        request.user.is_authenticated = lambda: True
        request.data = data
        response = set_preferences(request)
        self.assertEqual(response.status_code, 400)

    def test_skip_preferences_ajax_anonymous(self):
        request = self.factory.get(reverse("skipPreferences"))
        request.user = AnonymousUser()
        response = skip_preferences(request)
        self.assertEqual(response.status_code, 302)

    def test_skip_preferences_ajax_authenticated(self):
        request = self.factory.get(reverse("skipPreferences"))
        request.user = self.customUser
        request.user.is_authenticated = lambda: True
        response = skip_preferences(request)
        self.assertEqual(response.status_code, 302)

    def test_preferences_unauthenticated(self):
        # Make a GET request to the preferences view without logging in
        request = self.factory.get(reverse("preferences"))
        request.user = AnonymousUser()
        response = preferences(request)
        self.assertEqual(response.status_code, 302)

    def test_preferences_authenticated_no_preferences(self):
        # Make a GET request to the preferences view after logging in
        custom_user = CustomUser.objects.create(username="test", email="test@test.com")
        request = self.factory.get(reverse("preferences"))
        request.user = custom_user
        request.user.is_authenticated = lambda: True
        response = preferences(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, "users/preferences.html")
        self.assertEqual(response.context_data["preferences"], None)

    def test_preferences_authenticated_with_preferences(self):
        UserPreferences.objects.create(
            user=self.customUser,
            phone_number="1234567890",
            address="Test Address",
            diet="Vegetarian",
            height=170,
            weight=60,
            target_weight=55,
        )
        cuisine1 = Cuisine.objects.create(name="Chinese")
        cuisine2 = Cuisine.objects.create(name="Italian")
        allergy1 = Allergy.objects.create(name="Dairy")

        # Retrieve the created user preferences
        user_preferences = UserPreferences.objects.get(user=self.customUser)
        user_preferences.cuisines.add(cuisine1)
        user_preferences.cuisines.add(cuisine2)
        user_preferences.allergies.add(allergy1)

        request = self.factory.get(reverse("preferences"))
        request.user = self.customUser
        request.user.is_authenticated = lambda: True
        response = preferences(request)

        # Assert that the preferences are rendered correctly
        self.assertEqual(response.template_name, "users/preferences.html")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context_data["preferences"]["phone_number"], "1234567890"
        )
        self.assertEqual(
            response.context_data["preferences"]["address"], "Test Address"
        )
        self.assertEqual(response.context_data["preferences"]["diet"], "Vegetarian")
        # self.assertEqual(response.context_data['preferences']['cuisines'], ['Italian', 'Chinese'])
        self.assertEqual(response.context_data["preferences"]["allergies"], ["Dairy"])
        self.assertEqual(response.context_data["preferences"]["height"], 170)
        self.assertEqual(response.context_data["preferences"]["weight"], 60)
        self.assertEqual(response.context_data["preferences"]["target_weight"], 55)

    def test_update_custom_user_existing(self):
        # Simulate the user_logged_in event
        user_logged_in = Signal()
        user_logged_in.send(sender=self.customUser.__class__, user=self.customUser)

        # Retrieve the CustomUser object from the database
        custom_user = CustomUser.objects.get(email=self.customUser.email)

        # Verify that the CustomUser's last_login is updated
        self.assertTrue(
            custom_user.last_login > timezone.now() - timezone.timedelta(seconds=1)
        )

    def test_update_custom_user_new(self):
        customUser = CustomUser.objects.create(username="test", email="test@test.com")
        user_logged_in = Signal()
        # Simulate the user_logged_in event for a new user
        user_logged_in.send(sender=customUser.__class__, user=customUser)

        # Retrieve the CustomUser object from the database
        custom_user = CustomUser.objects.get(email=customUser.email)

        # Verify that a new CustomUser object is created with the correct data
        self.assertEqual(custom_user.email, customUser.email)
        self.assertEqual(custom_user.username, customUser.username)
        self.assertEqual(custom_user.preferences, False)

    def test_clean_email_unique(self):
        # Test that clean_email method raises ValidationError for existing email
        form_data = {
            "username": "test_user",
            "email": "test@example.com",
            "password": "testpassword",
        }
        form = UserSignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertEqual(form.errors["email"], ["Email already exists."])

    def test_clean_username_unique(self):
        # Test that clean_username method raises ValidationError for existing username
        form_data = {
            "username": "testuser",
            "email": "testing@example.com",
            "password": "testpassword",
        }
        form = UserSignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        self.assertEqual(form.errors["username"], ["Username already exists."])

    def test_update_custom_user_existing(self):
        # CustomUser.objects.create(username=self.user.username, email=self.user.email)
        request = self.factory.get('/')
        request.user = self.customUser
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()

        update_custom_user(CustomUser, self.customUser, request)
        custom_user = CustomUser.objects.get(username=self.customUser.username)

        self.assertEqual(custom_user.last_login.date(), timezone.now().date())
        self.assertEqual(request.session["check_user_preferences"], custom_user.preferences)
        self.assertEqual(request.session["username"], self.customUser.username)

    def test_update_custom_user_new(self):
        request = self.factory.get('/')
        request.user = self.customUser
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()

        update_custom_user(User, self.customUser, request)
        custom_user = CustomUser.objects.get(username=self.customUser.username)

        self.assertEqual(custom_user.last_login.date(), timezone.now().date())
        self.assertEqual(request.session["username"], self.customUser.username)

    @patch('users.signals.CustomUser.objects.create')
    @freeze_time("2024-04-10 16:39:55")
    def test_user_signed_up(self, mock_create):
        data = {"username": "testuser", "email": "test@otherexample.com"}
        request = self.factory.get('/')
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()

        user_signed_up(data, request)

        mock_create.assert_called_once_with(
            username=data["username"],
            email=data["email"],
            preferences=False,
            last_login=timezone.now(),
        )
        self.assertEqual(request.session["check_user_preferences"], "False")
        self.assertEqual(request.session["username"], data["username"])

    @freeze_time("2024-04-10 16:39:55")
    def test_update_custom_user_new_user(self):
        request = self.factory.get('/')
        User.objects.create_user(
            username="newuser", email="newuser@example.com", last_login=timezone.now()
        )
        request.user = User.objects.get(username="newuser")
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()

        update_custom_user(User, request.user, request)
        custom_user = CustomUser.objects.get(username=request.user.username)

        self.assertEqual(custom_user.last_login.date(), timezone.now().date())
        self.assertEqual(request.session["username"], request.user.username)

    @freeze_time("2024-04-10 16:39:55")
    def test_user_signed_up_no_mock(self):
        data = {"username": "testotheruser", "email": "test@someotherexample.com"}
        request = self.factory.get('/')
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()

        user_signed_up(data, request)

        custom_user = CustomUser.objects.get(username=data["username"])
        self.assertEqual(custom_user.last_login.date(), timezone.now().date())
        self.assertEqual(request.session["check_user_preferences"], "False")
        self.assertEqual(request.session["username"], data["username"])
