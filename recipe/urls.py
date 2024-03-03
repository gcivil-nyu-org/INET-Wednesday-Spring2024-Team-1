from django.urls import path
from . import views

app_name = 'recipe'

urlpatterns = [
    path('recipe/<int:recipe_id>/', views.recipe_info, name='recipe'),
]