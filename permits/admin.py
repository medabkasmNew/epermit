from django import forms
from django.contrib import admin

from .constants import PermitType
from .forms import FreeTextListField
from .models import EPermit


class EPermitAdminForm(forms.ModelForm):
    epermit_type = forms.MultipleChoiceField(
        choices=PermitType.choices,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    other_precautions = FreeTextListField(required=False)

    class Meta:
        model = EPermit
        fields = "__all__"


@admin.register(EPermit)
class EPermitAdmin(admin.ModelAdmin):
    form = EPermitAdminForm
    list_display = (
        "permit_number", "work_area", "status", "requester",
        "hse_supervisor", "start_expected", "end_expected", "types_display",
    )
    list_filter = ("status",)
    search_fields = ("permit_number", "work_area", "requester__badge_number")
    readonly_fields = ("permit_number", "requester", "created_at", "updated_at")

    @admin.display(description="Types")
    def types_display(self, obj):
        labels = dict(PermitType.choices)
        return ", ".join(labels.get(t, t) for t in obj.epermit_type) or "-"

    def save_model(self, request, obj, form, change):
        if not change:
            obj.requester = request.user  # the creator is the requester
        super().save_model(request, obj, form, change)