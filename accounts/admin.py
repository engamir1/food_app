from django.contrib import admin

# Register your models here.
from .models import CustomUser, UserProfile
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    list_display = ("email", "username", "role", "first_name", "last_name", "is_active")
    ordering = ("-date_joind",)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)
