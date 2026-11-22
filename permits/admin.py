from django.contrib import admin

from .models import ColdWork, EPermit, WorkAtHeight


class WorkAtHeightInline(admin.TabularInline):
    model = WorkAtHeight
    extra = 0


class ColdWorkInline(admin.TabularInline):
    model = ColdWork
    extra = 0


@admin.register(EPermit)
class EPermitAdmin(admin.ModelAdmin):
    list_display = (
        "permit_number", "work_area", "status", "requester",
        "hse_supervisor", "start_expected", "end_expected", "epermit_type",
    )
    list_filter = ("status",)
    search_fields = ("permit_number", "work_area", "requester__badge_number")
    readonly_fields = ("permit_number", "requester", "epermit_type", "created_at", "updated_at")
    inlines = [WorkAtHeightInline, ColdWorkInline]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.requester = request.user  # the creator is the requester
        super().save_model(request, obj, form, change)