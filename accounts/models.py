from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models


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
        extra_fields.setdefault("role", User.Role.ADMIN)
        return self._create_user(badge_number, password, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        OPERATOR = "operator", "Operator"
        TECHNICIEN = "technicien", "Technicien"
        FORMAN = "forman", "Forman"
        ENGINEER = "engineer", "Engineer"
        TEAM_LEADER = "team_leader", "Team leader"
        DEPARTEMENT_CHIEF = "departement_chief", "Departement chief"
        MANAGER = "manager", "Manager"
        ADMIN = "admin", "Admin"
    class Department(models.TextChoices):
        WIRERODE = 'wirerode', 'Wirerode'
        QA = 'qa', 'QA'
        LOGISTICS = 'logistics', 'Logistics'
        HEAVY_MACHINE = 'heavy_machine', 'Heavy Machine'
        HSM = 'hsm', 'HSM'
        CRM = 'crm', 'CRM'
        HSPM = 'hspm', 'HSPM'
        SMP1 = 'smp1', 'SMP1'
        SMP2 = 'smp2', 'SMP2'
        SMP3 = 'smp3', 'SMP3'
        SMP4 = 'smp4', 'SMP4'
        RM1 = 'rm1', 'RM1'
        RM2 = 'rm2', 'RM2'
        RM3 = 'rm3', 'RM3'
        DRI1 = 'dri1', 'DRI1'
        DRI2 = 'dri2', 'DRI2'
        DRI3 = 'dri3', 'DRI3'
        PELLET1 = 'pellet1', 'Pellet1'
        PELLET2 = 'pellet2', 'Pellet2'
        IT = 'it', 'IT'
        HOLDING = 'holding', 'Holding'
        ADMINISTRATION = 'administration', 'Administration'
        ASU1 = 'asu1', 'ASU1'
        ASU2 = 'asu2', 'ASU2'
        ASU3 = 'asu3', 'ASU3'
        WTP1 = 'wtp1', 'WTP1'
        WTP2 = 'wtp2', 'WTP2'
        WTP3 = 'wtp3', 'WTP3'
        WTP4 = 'wtp4', 'WTP4'
        LIME1 = 'lime1', 'Lime1'
        LIME2 = 'lime2', 'Lime2'
        PIPE = 'pipe', 'Pipe'
        SHRIDER = 'shrider', 'Shrider'
        HARSCO = 'harsco', 'Harsco'
        TRANSPORTATION = 'transportation', 'Transportation'
        CEAW = 'ceaw', 'CEAW'
        MOYEN_GENERAUX = 'general_services', 'General Services'
        OTHER = 'other', 'Other'    
    username = None  # removed, the badge number is the login

    badge_number = models.CharField(
        max_length=5,
        unique=True,
        validators=[RegexValidator(r"^\d{5}$", "Badge number must be exactly 5 digits.")],
    )
    # first_name, last_name, email, password come from AbstractUser
    department = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.OPERATOR)

    USERNAME_FIELD = "badge_number"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return self.badge_number