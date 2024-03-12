from django.db import models

# Create your models here.


class CustomUser(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField(max_length=150, primary_key=True)
    preferences = models.BooleanField(default=False)


class Cuisine(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Allergy(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class UserPreferences(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(
        max_length=15
    )  # Assuming the phone number format (including country code)
    address = models.CharField(max_length=255)
    DIET_CHOICES = [
        ("vegetarian", "Vegetarian"),
        ("non-vegetarian", "Non-vegetarian"),
        ("vegan", "Vegan"),
    ]
    diet = models.CharField(max_length=20, choices=DIET_CHOICES, null=True)
    cuisines = models.ManyToManyField(
        Cuisine, null=True
    )  # Allow multiple cuisine selections
    allergies = models.ManyToManyField(
        Allergy, null=True
    )  # Allow multiple allergy selections
    height = models.PositiveIntegerField()  # Assuming height is in cm
    weight = models.PositiveIntegerField()  # Assuming weight is in lbs
    target_weight = models.PositiveIntegerField()  # Assuming target weight is in lbs
