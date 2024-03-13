from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import models
from .models import CustomUser, UserPreferences, Cuisine, Allergy
from django.utils import timezone

class UserPreferencesTestCase(TestCase):
    def setUp(self):
        # Create a test user
        # self.user = User.objects.create_user(username='testuser', email='test@example.com', last_login=timezone.now())
        self.customUser = CustomUser.objects.create(username='testuser', email='test@example.com')
        # Create test cuisines and allergies
        self.cuisine1 = Cuisine.objects.create(name='Chinese')
        self.cuisine2 = Cuisine.objects.create(name='Indian')
        self.allergy1 = Allergy.objects.create(name='Dairy')
        self.allergy2 = Allergy.objects.create(name='Nuts')

    def test_create_user_preferences(self):
        # Create user preferences
        UserPreferences.objects.create(
            user=self.customUser,
            phone_number='1234567890',
            address='Test Address',
            diet='vegetarian',
            height=170,
            weight=150,
            target_weight=140
        )

        # Retrieve the created user preferences
        user_preferences = UserPreferences.objects.get(user=self.customUser)
        user_preferences.cuisines.add(self.cuisine1)
        user_preferences.allergies.add(self.allergy1)

        # Check if the created user preferences match the provided data
        self.assertEqual(user_preferences.phone_number, '1234567890')
        self.assertEqual(user_preferences.address, 'Test Address')
        self.assertEqual(user_preferences.diet, 'vegetarian')
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
            phone_number='1234567890',
            address='Test Address',
            diet='vegetarian',
            height=170,
            weight=150,
            target_weight=140
        )

        # Update user preferences
        user_preferences.diet = 'vegan'
        user_preferences.save()

        # Retrieve the updated user preferences
        updated_preferences = UserPreferences.objects.get(user=self.customUser)

        # Check if the diet field is updated
        self.assertEqual(updated_preferences.diet, 'vegan')

    def test_delete_user_preferences(self):
        # Create user preferences
        user_preferences = UserPreferences.objects.create(
            user=self.customUser,
            phone_number='1234567890',
            address='Test Address',
            diet='vegetarian',
            height=170,
            weight=150,
            target_weight=140
        )

        # Delete user preferences
        user_preferences.delete()

        # Ensure the preferences are deleted
        with self.assertRaises(UserPreferences.DoesNotExist):
            UserPreferences.objects.get(user=self.customUser)

    def test_form_submission_valid_data_anonymous(self):
        self.client = Client()
        data = {
            'phone': '1234567890',
            'address': 'Test Address',
            'diet': 'vegetarian',
            'cuisine': ['Indian', 'Italian'],
            'allergies': ['Dairy', 'Nuts'],
            'height': '170',
            'weight': '150',
            'targetWeight': '140'
        }
        response = self.client.post(reverse('setPreferences'), data)
        self.assertEqual(response.status_code, 302)  # Redirects to login page for anonymous users

    def test_skip_preferences_ajax(self):
        # self.client.force_login(self.customUser)
        
        response = self.client.get(reverse('skipPreferences'))
        self.assertEqual(response.status_code, 302)
