from django.core.validators import RegexValidator

validate_algerian_phone = RegexValidator(
    regex=r"^0[567]\d{8}$",
    message="Enter an Algerian mobile number.",
)