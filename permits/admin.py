from django import forms
from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.html import format_html

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
        "hse_supervisor", "start_expected", "end_expected", "types_display", "details_link",
    )
    list_filter = ("status",)
    search_fields = ("permit_number", "work_area", "requester__badge_number")
    readonly_fields = ("permit_number", "requester", "created_at", "updated_at")

    @admin.display(description="Types")
    def types_display(self, obj):
        labels = dict(PermitType.choices)
        return ", ".join(labels.get(t, t) for t in obj.epermit_type) or "-"

    @admin.display(description="Details")
    def details_link(self, obj):
        url = reverse("admin:permits_epermit_detail", args=[obj.pk])
        return format_html('<a href="{}">View</a>', url)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.requester = request.user  # the creator is the requester
        super().save_model(request, obj, form, change)

    def get_urls(self):
        custom = [
            path(
                "<int:object_id>/detail/",
                self.admin_site.admin_view(self.detail_view),
                name="permits_epermit_detail",
            ),
        ]
        return custom + super().get_urls()

    def detail_view(self, request, object_id):
        obj = self.get_object(request, object_id)
        if obj is None:
            raise Http404("Permit not found")
        if not self.has_view_permission(request, obj):
            raise PermissionDenied

        labels = dict(PermitType.choices)
        context = {
            **self.admin_site.each_context(request),
            "opts": self.model._meta,
            "original": obj,
            "title": f"Permit {obj.permit_number}",
            "type_labels": [labels.get(t, t) for t in obj.epermit_type],
        }
        return TemplateResponse(request, "admin/permits/epermit_detail.html", context)