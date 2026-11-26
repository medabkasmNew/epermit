from django.conf import settings
from django.db import models, transaction
from django.utils import timezone
from .constants import PermitStatus
from accounts.constants import Department
from .validators import (
    validate_additional_certificates,
    validate_free_text_list,
    validate_mandatory_ppe,
    validate_permit_types,
)


class EPermit(models.Model):
    # Section 01 - Permit Information
    permit_number = models.CharField(max_length=20, unique=True, null=True, blank=True, editable=False)
    start_expected = models.DateTimeField()
    end_expected = models.DateTimeField()
    work_area = models.CharField(max_length=255,choices=Department.choices,default=Department.OTHER)
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

    mandatory_ppe = models.JSONField(
        default=list,
        validators=[validate_mandatory_ppe],
    )  # the 5 mandatory codes + free-text extras
    additional_ppe = models.JSONField(
        default=list,
        blank=True,
        validators=[validate_free_text_list],
    )  # ticked option codes + free-text extras, may be empty

    additional_certificates = models.JSONField(
        default=list,
        blank=True,
        validators=[validate_additional_certificates],
    )  # e.g. ["work_at_height", "x_ray_work"]; [] means none required

    status = models.CharField(max_length=10, choices=PermitStatus.choices, default=PermitStatus.PENDING)
    epermit_type = models.JSONField(
        default=list,
        blank=True,
        validators=[validate_permit_types],
    )  # e.g. ["work_at_height", "cold_work"]
    other_precautions = models.JSONField(
        default=list,
        blank=True,
        validators=[validate_free_text_list],
    )  # free-text items, duplicates allowed

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