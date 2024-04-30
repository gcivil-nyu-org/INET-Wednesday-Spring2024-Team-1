from django.urls import path
from django.contrib.auth import views as auth_views
from .views import orders_view, order_items, change_order_status, login_redirect_admin, admin_login

urlpatterns = [
    # path("login/", auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('adminLogin/', admin_login, name='admin_login'),
    path('orders/', orders_view, name='orders'),
    path("", login_redirect_admin, name='login_admin'),
    path('order-items/<int:order_id>/', order_items, name='order_items'),
    path('change-order-status/<int:order_id>/', change_order_status, name='change_order_status'),
]