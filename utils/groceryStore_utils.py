from groceryStore.models import Ingredient
import random


def grocery_addition(groceryId, groceryName):
    price = round(random.uniform(0.5, 10.0), 2)  # Generating random price between 0.5 and 10.0
    stock = random.randint(0, 100)  # Generating random stock between 0 and 100
    ingredient = Ingredient.objects.create(iid=groceryId, iname=groceryName, price=price, stock=stock)
    ingredient.save()
