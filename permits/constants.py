from django.db import models


class PermitType(models.TextChoices):
    """Predefined options for EPermit.epermit_type. Add one line per new type."""
    WORK_AT_HEIGHT = "work_at_height", "Work at height"
    COLD_WORK = "cold_work", "Cold work"
    HOT_WORK = "hot_work", "Hot work"
    CONFINED_SPACE = "confined_space", "Confined space"
    ELECTRICAL_WORK = "electrical_work", "Electrical work"
    EXCAVATION_WORK = "excavation_work", "Excavation work"
    LIFTING_OPERATION = "lifting_operation", "Lifting operation"


class PermitStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    CLOSED = "closed", "Closed"
    REJECTED = "rejected", "Rejected"
    PAUSED = "paused", "Paused"


class MandatoryPPE(models.TextChoices):
    """Always required on site. Must all be present in EPermit.mandatory_ppe."""
    SAFETY_HELMET = "safety_helmet", "Safety helmet"
    SAFETY_SHOES = "safety_shoes", "Safety shoes"
    SAFETY_GLASSES = "safety_glasses", "Safety glasses"
    SAFETY_VEST = "safety_vest", "Safety vest"
    HEARING_PROTECTION = "hearing_protection", "Hearing protection"


class AdditionalPPE(models.TextChoices):
    """Offered as checkboxes. The user ticks the ones the job needs."""
    LIFE_JACKET = "life_jacket", "Life jacket"
    SAFETY_HARNESS = "safety_harness", "Safety harness"
    GLOVES = "gloves", "Gloves"
    MASKS = "masks", "Masks"
    FACE_PROTECTION_VISOR = "face_protection_visor", "Face protection visor"