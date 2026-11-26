from django.db import models


class PermitType(models.TextChoices):
    """Predefined options for EPermit.epermit_type. Add one line per new type."""
    WORK_AT_HEIGHT = "work_at_height", "Work at height"
    COLD_WORK = "cold_work", "Cold work"


class PermitStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    CLOSED = "closed", "Closed"
    REJECTED = "rejected", "Rejected"
    PAUSED = "paused", "Paused"