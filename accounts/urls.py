from django.urls import path
from .views import (
    dashboard,
    login,
    logout,
    register_user,
    register_vendor,
    customer_dashboard,
    vendor_dashboard,
    activate,
    forget_password,
    reset_password,
    reset_password_token,
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
    # activate user
    path("activate/<uidb64>/<token>", activate, name="activate"),
    # password
    path("forget_password/", forget_password, name="forget_password"),
    path("reset_password/", reset_password, name="reset_password"),
    # link that send token to users email
    path(
        "reset_password_token/<uidb64>/<token>/",
        reset_password_token,
        name="reset_password_token",
    ),
]
