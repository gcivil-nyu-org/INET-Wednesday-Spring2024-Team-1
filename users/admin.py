from django.contrib import admin

# Register your models here.

from .models import UserPreferences, CustomUser, Cuisine, Allergy

admin.site.register(UserPreferences)
admin.site.register(CustomUser)
admin.site.register(Cuisine)
admin.site.register(Allergy)
