from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Grocery
from .serializers import GrocerySerializer


@api_view(["GET"])
def get_grocery_details(request, gname):
    try:
        grocery = Grocery.objects.get(gname=gname)
        serializer = GrocerySerializer(grocery)
        return Response(serializer.data)
    except Grocery.DoesNotExist:
        return Response({"message": "Grocery not found"}, status=404)
