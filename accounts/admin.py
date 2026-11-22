from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("badge_number", "first_name", "last_name", "email",
                  "department", "phone_number", "role")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    ordering = ("badge_number",)
    list_display = ("badge_number", "first_name", "last_name", "department", "role", "is_active")
    list_filter = ("role", "department", "is_active", "is_staff")
    search_fields = ("badge_number", "first_name", "last_name", "email")

    fieldsets = (
        (None, {"fields": ("badge_number", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email", "phone_number")}),
        ("Work", {"fields": ("department", "role")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser",
                                    "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("badge_number", "first_name", "last_name", "email",
                       "department", "phone_number", "role",
                       "password1", "password2"),
        }),
    )