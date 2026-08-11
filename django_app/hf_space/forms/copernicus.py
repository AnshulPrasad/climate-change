import json
from pathlib import Path
from django import forms
from django_app.hf_space.constants.copernicus import COPERNICUS_VARIABLE_CHOICES

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schemas" / "copernicus.json"

class DynamicCDSFormFactory:
    @staticmethod
    def _get_choice_generator(field_spec: dict) -> list:
        if "choices" in field_spec:
            return field_spec["choices"]
        elif "choices_category" in field_spec:
            return COPERNICUS_VARIABLE_CHOICES
        elif "choices_range" in field_spec:
            start, end = field_spec["choices_range"]
            return [(str(i), str(i)) for i in range(start, end)]
        elif field_spec.get("choices_format") == "month":
            return [(f"{m:02d}", f"{m:02d}") for m in range(1, 13)]
        elif field_spec.get("choices_format") == "day":
            return [(f"{d:02d}", f"{d:02d}") for d in range(1, 32)]
        elif field_spec.get("choices_format") == "time":
            return [(f"{h:02d}:00", f"{h:02d}:00") for h in range(24)]
        return []

    @classmethod
    def create_form(cls, data: dict = None) -> forms.Form:
        dataset_id = "reanalysis-era5-single-levels"
        with open(SCHEMA_PATH, "r") as f:
            schemas = json.load(f)

        schema = schemas[dataset_id]
        fields = {}

        for field_name, spec in schema.items():
            field_type = spec["type"]
            default_val = spec.get("default")
            label = field_name.replace("_", " ").title()

            if field_type == "choice":
                choices = cls._get_choice_generator(spec)
                fields[field_name] = forms.ChoiceField(
                    choices=choices,
                    initial=default_val,
                    label=label
                )
            elif field_type in ("multiple_choice", "categorized_multiple_choice"):
                choices = cls._get_choice_generator(spec)
                fields[field_name] = forms.MultipleChoiceField(
                    choices=choices,
                    initial=default_val,
                    label=label,
                    widget=forms.CheckboxSelectMultiple
                )
            elif field_type == "char":
                fields[field_name] = forms.CharField(
                    initial=default_val,
                    label=label
                )

        form_class = type(f"Dynamic_{dataset_id.title()}_Form", (forms.Form,), fields)
        return form_class(data=data)