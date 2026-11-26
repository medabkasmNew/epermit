from html import escape
import json

from django import forms
from django.utils.safestring import mark_safe

from .models import EPermit

SCRIPT = """
(function () {
  var root = document.currentScript.parentElement;
  var items = root.querySelector(".precautions-items");
  root.querySelector(".add-precaution").addEventListener("click", function () {
    var row = document.createElement("div");
    row.className = "precaution-row";
    row.style.marginBottom = "6px";
    var input = document.createElement("input");
    input.type = "text";
    input.name = __NAME__;
    input.maxLength = 255;
    input.style.width = "60%";
    var remove = document.createElement("button");
    remove.type = "button";
    remove.className = "remove-precaution";
    remove.textContent = "Remove";
    remove.style.marginLeft = "6px";
    row.appendChild(input);
    row.appendChild(remove);
    items.appendChild(row);
    input.focus();
  });
  items.addEventListener("click", function (e) {
    if (e.target.classList.contains("remove-precaution")) {
      e.target.parentElement.remove();
    }
  });
})();
"""


class PrecautionsWidget(forms.Widget):
    """A list of free texts: one text input per item and a "+ Add" button."""

    def value_from_datadict(self, data, files, name):
        return data.getlist(name)

    def render(self, name, value, attrs=None, renderer=None):
        items = [str(v) for v in value] if isinstance(value, (list, tuple)) else []
        if not items:
            items = [""]  # start with one empty field

        rows = "".join(
            '<div class="precaution-row" style="margin-bottom:6px">'
            f'<input type="text" name="{escape(name)}" value="{escape(item)}" '
            'maxlength="255" style="width:60%">'
            '<button type="button" class="remove-precaution" style="margin-left:6px">Remove</button>'
            "</div>"
            for item in items
        )
        script = SCRIPT.replace("__NAME__", json.dumps(name))
        return mark_safe(
            '<div class="precautions-widget">'
            f'<div class="precautions-items">{rows}</div>'
            '<button type="button" class="add-precaution">+ Add</button>'
            f"<script>{script}</script>"
            "</div>"
        )


class FreeTextListField(forms.Field):
    """A list of free-text items. Duplicates are kept, empty items are dropped."""
    widget = PrecautionsWidget

    def to_python(self, value):
        return [v.strip() for v in (value or []) if v and v.strip()]


class EPermitForm(forms.ModelForm):
    other_precautions = FreeTextListField(required=False)

    class Meta:
        model = EPermit
        fields = ["start_expected", "end_expected", "work_area", "job_description"]
        widgets = {
            "start_expected": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
            "end_expected": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
            "job_description": forms.Textarea(attrs={"rows": 4}),
        }