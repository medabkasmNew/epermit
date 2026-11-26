from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from .constants import Role,Department

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, badge_number, password, **extra_fields):
        if not badge_number:
            raise ValueError("The badge number is required")
        user = self.model(badge_number=badge_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, badge_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(badge_number, password, **extra_fields)

    def create_superuser(self, badge_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", Role.ADMIN)
        return self._create_user(badge_number, password, **extra_fields)


class User(AbstractUser):

    username = None  # removed, the badge number is the login

    badge_number = models.CharField(
        max_length=4,
        unique=True,
        validators=[RegexValidator(r"^\d{4}$", "Badge number must be exactly 4 digits.")],
    )
    # first_name, last_name, email, password come from AbstractUser
    department = models.CharField(max_length=30, choices=Department.choices)
    phone_number = models.CharField(max_length=20)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.OPERATOR)

    USERNAME_FIELD = "badge_number"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return self.badge_number