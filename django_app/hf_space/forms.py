from django import forms

class CopernicusForm(forms.Form):
    """Specific query parameters for the Copernicus Climate Data Store API."""
    dataset = forms.ChoiceField(
        choices=[('reanalysis-era5-single-levels', 'ERA5 Single Levels')],
        initial='reanalysis-era5-single-levels',
        label="Dataset"
    )

    product_type = forms.MultipleChoiceField(
        choices=[('reanalysis', 'Reanalysis')],
        initial=['reanalysis'],
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    variable = forms.MultipleChoiceField(
        choices=[('2m_temperature', '2m Temperature')],  # Append additional variables as required
        initial=['2m_temperature'],
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    year = forms.MultipleChoiceField(
        choices=[(str(y), str(y)) for y in range(1940, 2027)],
        initial=['2024'],
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    month = forms.MultipleChoiceField(
        choices=[(f"{m:02d}", f"{m:02d}") for m in range(1, 13)],
        initial=['03'],
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    day = forms.MultipleChoiceField(
        choices=[(f"{d:02d}", f"{d:02d}") for d in range(1, 32)],
        initial=['01'],
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    time = forms.MultipleChoiceField(
        choices=[(f"{h:02d}:00", f"{h:02d}:00") for h in range(24)],
        initial=['13:00'],
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    area = forms.CharField(
        initial='30, 70, 8, 90',
        help_text="Format: North, West, South, East",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    data_format = forms.ChoiceField(
        choices=[('grib', 'GRIB'), ('netcdf', 'NetCDF')],
        initial='grib',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    download_format = forms.ChoiceField(
        choices=[('unarchived', 'Unarchived'), ('zip', 'ZIP')],
        initial='unarchived',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')

        if start and end and start > end:
            raise forms.ValidationError('Start date must precede end date')
        return cleaned_data