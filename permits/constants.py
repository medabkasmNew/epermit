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