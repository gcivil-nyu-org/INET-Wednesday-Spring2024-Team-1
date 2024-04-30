from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from groceryStore.models import Order
import json
from django.core.serializers import serialize
from groceryStore.views import get_grocery_details_no_api
from FoodSync.settings import BASE_API_URL
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


base_url = BASE_API_URL

def login_redirect_admin(request):
    if request.user.is_superuser:
        return redirect('orders')
    return render(request, 'store/login.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        print(user.is_superuser)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('orders')
            else:
                return render(request, 'store/login.html')
        else:
            return render(request, 'store/login.html', {'error': 'Invalid username or password'})

    return render(request, 'store/login.html')

@login_required
def orders_view(request):
    status = request.GET.get('status')
    if status in ['completed', 'cancelled', 'pending']:
        orders = Order.objects.filter(status=status).order_by('-date')
    else:
        orders = Order.objects.all().order_by('-date')

    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)

    # orders_json = serialize('json', orders)

    status_list = ['completed', 'cancelled']

    return render(request, 'store/orders.html', {'orders': orders, 'status': status, 'status_list': status_list})

@login_required
def order_items(request, order_id):
    order = Order.objects.get(pk=order_id)
    items = list(order.orderitem_set.values())
    for item in items:
        item['grocery'] = get_grocery_details_no_api(item['grocery_id'])
    print(items)
    return JsonResponse(items, safe=False)

@csrf_exempt
@login_required
def change_order_status(request, order_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_status = data.get('status')
        if new_status is not None:
            order = Order.objects.get(pk=order_id)
            order.status = new_status
            order.save()
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return HttpResponse('Invalid status', status=400)