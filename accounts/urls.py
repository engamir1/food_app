from django.urls import path
from .views import register_user ,register_vendor

urlpatterns = [
    path("register_new_user", register_user, name="register_new_user"),
    path("register_new_vendor", register_vendor, name="register_new_vendor"),

]
