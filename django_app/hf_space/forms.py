from django import forms

SOURCE_CHOICES = [
    ("home", "Home"),
    ("copernicus", "Copernicus"),
    ("earth_engine", "Google Earth Engine"),
    ("hugging_face", "Hugging Face"),
    ("nasa", "NASA Power / Earthdata"),
    ("noaa", "NOAA"),
    ("owid", "Our World in Data"),
    ("world_bank", "World Bank"),
]

class ClimateDataConfigForm(forms.Form):
    source = forms.ChoiceField(
        choices=SOURCE_CHOICES,
        widget = forms.HiddenInput() # Controlled by the sidebar section
    )
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type':'date', 'class':'form-control'})
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    dataset = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City / Coordinates'})
    )
    location = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'India'})
    )
    station = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Station ID / Name'})
    )

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')

        if start and end and start > end:
            raise forms.ValidationError('Start date must precede end date')
        return cleaned_data