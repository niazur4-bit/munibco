from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ["username", "email", "role", "phone", "company_name", "is_staff"]
    list_filter = ["role", "is_staff"]
    fieldsets = UserAdmin.fieldsets + (
        ("Munib and Co Info", {"fields": ("role", "phone", "company_name")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Munib and Co Info", {"fields": ("role", "phone", "company_name", "email")}),
    )
