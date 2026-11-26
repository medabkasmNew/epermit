from django.core.exceptions import ValidationError

from .constants import PermitType , MandatoryPPE

MAX_ITEM_LENGTH = 50


def validate_free_text_list(value):
    """other_precautions: a list of non-empty texts. Duplicates are allowed."""
    if not isinstance(value, list):
        raise ValidationError("Must be a list of texts.")
    for position, item in enumerate(value, start=1):
        if not isinstance(item, str):
            raise ValidationError(f"Item {position} must be text.")
        if not item.strip():
            raise ValidationError(f"Item {position} cannot be empty.")
        if len(item) > MAX_ITEM_LENGTH:
            raise ValidationError(f"Item {position} is longer than {MAX_ITEM_LENGTH} characters.")


def validate_permit_types(value):
    """epermit_type: a list of predefined options, each at most once."""
    if not isinstance(value, list):
        raise ValidationError("Must be a list of permit types.")

    allowed = set(PermitType.values)
    for item in value:
        if item not in allowed:
            raise ValidationError(f"'{item}' is not a valid permit type.")

    if len(value) != len(set(value)):
        raise ValidationError("A permit type can only appear once.")

def validate_mandatory_ppe(value):
    """mandatory_ppe: free-text list rules, and all mandatory options must be present."""
    validate_free_text_list(value)
    missing = [label for code, label in MandatoryPPE.choices if code not in value]
    if missing:
        raise ValidationError("Missing mandatory PPE: " + ", ".join(missing) + ".")

def validate_additional_certificates(value):
    """additional_certificates: a list of predefined options, each at most once. Empty is allowed."""
    if not isinstance(value, list):
        raise ValidationError("Must be a list of certificates.")

    allowed = set(AdditionalCertificate.values)
    for item in value:
        if item not in allowed:
            raise ValidationError(f"'{item}' is not a valid certificate.")

    if len(value) != len(set(value)):
        raise ValidationError("A certificate can only appear once.")