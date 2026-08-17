import json
from pathlib import Path
from django import forms
SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schemas" / "faostat.json"

class FAOSTATFormFactory:

    @classmethod
    def create_form(cls, dataset_id: str, data: dict = None) -> forms.Form:
        with open(SCHEMA_PATH, "r") as f: schemas = json.load(f)
        fields = {}
        for field_name, spec in schemas[dataset_id].items():
            fields[field_name] = forms.ChoiceField(choices=spec.get("choices", []), initial=spec.get("default"), label=field_name.replace("_", " ").title())
        return type(f"FAOSTAT_{dataset_id.replace('-', '_').title()}_Form", (forms.Form,), fields)(data=data)