import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FoodSync.settings')
django.setup()

from django.contrib.auth.models import User
from groceryStore.models import Grocery, Order, OrderItem, UserProfile

# Function to create users
def create_users():
    users = [
        {'username': 'user1', 'password': 'password1', 'email': 'user1@example.com'},
        {'username': 'user2', 'password': 'password2', 'email': 'user2@example.com'},
        # Add more users as needed
    ]
    for user_data in users:
        User.objects.create_user(**user_data)

# Function to create groceries
def create_groceries():
    groceries = [
        {'gname': 'Apple', 'price': 1.50, 'stock': 100},
        {'gname': 'Banana', 'price': 0.75, 'stock': 150},
        {'gname': 'Orange', 'price': 1.20, 'stock': 120},
        {'gname': 'Grapes', 'price': 2.00, 'stock': 80},
        {'gname': 'Strawberry', 'price': 3.50, 'stock': 60},
        {'gname': 'Blueberry', 'price': 4.00, 'stock': 70},
        {'gname': 'Mango', 'price': 2.50, 'stock': 90},
        {'gname': 'Pineapple', 'price': 2.75, 'stock': 100},
        {'gname': 'Watermelon', 'price': 5.00, 'stock': 40},
        {'gname': 'Kiwi', 'price': 1.80, 'stock': 110},
        {'gname': 'Peach', 'price': 2.25, 'stock': 95},
        {'gname': 'Pear', 'price': 1.70, 'stock': 85},
        {'gname': 'Plum', 'price': 1.90, 'stock': 75},
        {'gname': 'Cherry', 'price': 3.20, 'stock': 55},
        {'gname': 'Raspberry', 'price': 4.50, 'stock': 65},
        {'gname': 'Blackberry', 'price': 4.20, 'stock': 50},
        {'gname': 'Lemon', 'price': 0.90, 'stock': 130},
        {'gname': 'Lime', 'price': 1.00, 'stock': 125},
        {'gname': 'Coconut', 'price': 3.75, 'stock': 45},
        {'gname': 'Avocado', 'price': 2.80, 'stock': 105},
        {'gname': 'Tomato', 'price': 1.25, 'stock': 140},
        {'gname': 'Cucumber', 'price': 0.60, 'stock': 180},
        {'gname': 'Carrot', 'price': 0.50, 'stock': 200},
        {'gname': 'Lettuce', 'price': 1.10, 'stock': 170},
        {'gname': 'Spinach', 'price': 1.30, 'stock': 160},
        {'gname': 'Broccoli', 'price': 1.80, 'stock': 130},
        {'gname': 'Cauliflower', 'price': 1.70, 'stock': 140},
        {'gname': 'Bell Pepper', 'price': 1.40, 'stock': 150},
        {'gname': 'Eggplant', 'price': 1.60, 'stock': 120},
        {'gname': 'Zucchini', 'price': 1.20, 'stock': 170},
        {'gname': 'Potato', 'price': 0.80, 'stock': 220},
        {'gname': 'Onion', 'price': 0.75, 'stock': 210},
        {'gname': 'Garlic', 'price': 0.70, 'stock': 200},
        {'gname': 'Ginger', 'price': 1.00, 'stock': 180},
        {'gname': 'Mushroom', 'price': 2.00, 'stock': 110},
        {'gname': 'Celery', 'price': 0.90, 'stock': 190},
        {'gname': 'Asparagus', 'price': 1.80, 'stock': 100},
        {'gname': 'Artichoke', 'price': 2.50, 'stock': 80},
        {'gname': 'Radish', 'price': 0.70, 'stock': 210},
        {'gname': 'Bean', 'price': 1.00, 'stock': 160},
        {'gname': 'Pea', 'price': 0.95, 'stock': 170},
        {'gname': 'Corn', 'price': 0.80, 'stock': 190},
        {'gname': 'Pumpkin', 'price': 3.00, 'stock': 60},
        {'gname': 'Squash', 'price': 2.00, 'stock': 90},
        {'gname': 'Sweet Potato', 'price': 1.50, 'stock': 120},
        {'gname': 'Beetroot', 'price': 1.20, 'stock': 150},
        {'gname': 'Turnip', 'price': 1.00, 'stock': 170},
        {'gname': 'Rutabaga', 'price': 1.10, 'stock': 160},
        {'gname': 'Parsnip', 'price': 1.30, 'stock': 140},
        {'gname': 'Kale', 'price': 1.25, 'stock': 130},
        {'gname': 'Swiss Chard', 'price': 1.40, 'stock': 120},
        {'gname': 'Collard Greens', 'price': 1.30, 'stock': 140},
        {'gname': 'Mustard Greens', 'price': 1.35, 'stock': 135},
        {'gname': 'Bok Choy', 'price': 1.20, 'stock': 150},
        {'gname': 'Cabbage', 'price': 1.00, 'stock': 180},
        {'gname': 'Brussels Sprouts', 'price': 1.50, 'stock': 100},
        {'gname': 'Okra', 'price': 1.10, 'stock': 170},
        {'gname': 'Leek', 'price': 1.25, 'stock': 130},
        {'gname': 'Scallion', 'price': 1.00, 'stock': 160},
        {'gname': 'Green Bean', 'price': 1.20, 'stock': 150},
        {'gname': 'Snap Pea', 'price': 1.00, 'stock': 180},
        {'gname': 'Snow Pea', 'price': 1.10, 'stock': 170},
        {'gname': 'Watercress', 'price': 1.30, 'stock': 140},
        {'gname': 'Radicchio', 'price': 1.40, 'stock': 120}
        # Add more groceries as needed
    ]
    for grocery_data in groceries:
        Grocery.objects.create(**grocery_data)

# Function to create orders
def create_orders():
    orders = [
        {'user': User.objects.get(username='user1'), 'total_price': 10.50, 'calories': 500, 'recipe': 'Recipe 1'},
        {'user': User.objects.get(username='user2'), 'total_price': 8.75, 'calories': 400, 'recipe': 'Recipe 2'},
        # Add more orders as needed
    ]
    for order_data in orders:
        order = Order.objects.create(**order_data)
        # Add order items
        OrderItem.objects.create(order=order, grocery=Grocery.objects.get(gname='Apple'), quantity=5)
        OrderItem.objects.create(order=order, grocery=Grocery.objects.get(gname='Banana'), quantity=10)
        # Add more order items as needed

# Function to create user profiles
def create_user_profiles():
    user_profiles = [
        {'user': User.objects.get(username='user1'), 'contact': '1234567890', 'addr': 'Address 1', 'email': 'user1@example.com'},
        {'user': User.objects.get(username='user2'), 'contact': '9876543210', 'addr': 'Address 2', 'email': 'user2@example.com'},
        # Add more user profiles as needed
    ]
    for profile_data in user_profiles:
        UserProfile.objects.create(**profile_data)

# Call functions to create data
# create_users()
create_groceries()
# create_orders()
# create_user_profiles()

print("Data populated successfully!")
