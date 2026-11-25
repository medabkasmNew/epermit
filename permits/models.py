from django.conf import settings
from django.db import models, transaction
from django.utils import timezone


class PermitType(models.TextChoices):
    """Predefined work permit types."""

    WORK_AT_HEIGHT = "work_at_height", "Work at height"
    COLD_WORK = "cold_work", "Cold work"
    HOT_WORK = "hot_work", "Hot work"
    CONFINED_SPACE_ENTRY = "confined_space_entry", "Confined space entry"
    ELECTRICAL_WORK = "electrical_work", "Electrical work"
    EXCAVATION_WORK = "excavation_work", "Excavation work"
    LIFTING_OPERATION = "lifting_operation", "Lifting operation"


class EPermit(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending"
        APPROVED = "approved"
        CLOSED = "closed"
        REJECTED = "rejected"
        PAUSED = "paused"

    # Section 01 - Permit Information
    permit_number = models.CharField(max_length=20, unique=True, null=True, blank=True, editable=False)
    start_expected = models.DateTimeField()
    end_expected = models.DateTimeField()
    work_area = models.CharField(max_length=255)
    job_description = models.TextField()

    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="epermits_requested",
    )
    hse_supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="epermits_supervised",
    )

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    epermit_type = models.JSONField(default=list, blank=True)  # e.g. ["work_at_height", "cold_work"]
    other_precautions = models.JSONField(default=list, blank=True)  # free-text items, duplicates allowed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(end_expected__gt=models.F("start_expected")),
                name="epermit_end_after_start",
            ),
        ]

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)
            if not self.permit_number:
                self.permit_number = f"EP-{timezone.now():%Y}-{self.pk:06d}"
                super().save(update_fields=["permit_number"])

    def __str__(self):
        return self.permit_number or f"EPermit {self.pk}"