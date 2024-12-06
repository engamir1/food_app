from django.urls import path
from .views import (
    dashboard,
    login,
    logout,
    register_user,
    register_vendor,
    customer_dashboard,
    vendor_dashboard,
)


app_name = "accounts"
urlpatterns = [
    path("register_new_user/", view=register_user, name="register_new_user"),
    path("register_new_vendor/", view=register_vendor, name="register_new_vendor"),
    path("login/", view=login, name="login"),
    path("logout/", view=logout, name="logout"),
    path("customer_dashboard/", view=customer_dashboard, name="customer_dashboard"),
    path("vendor_dashboard/", view=vendor_dashboard, name="vendor_dashboard"),
    path("dashboard/", view=dashboard, name="dashboard"),
]
