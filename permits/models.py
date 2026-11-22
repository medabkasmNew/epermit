from django.conf import settings
from django.db import models, transaction
from django.utils import timezone


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
    epermit_type = models.JSONField(default=list, blank=True)

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

    @property
    def types(self):
        """One-to-many: all rows from all type tables linked to this permit."""
        from itertools import chain
        return list(chain(
            self.workatheight_set.all(),
            self.coldwork_set.all(),
        ))

    def __str__(self):
        return self.permit_number or f"EPermit {self.pk}"


class WorkAtHeight(models.Model):
    epermit = models.ForeignKey(EPermit, on_delete=models.CASCADE)
    applicable = models.BooleanField(default=True)


class ColdWork(models.Model):
    epermit = models.ForeignKey(EPermit, on_delete=models.CASCADE)
    applicable = models.BooleanField(default=True)