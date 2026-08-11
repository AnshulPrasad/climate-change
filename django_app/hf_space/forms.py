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
        label='Product Type',
        widget=forms.CheckboxSelectMultiple
    )

    variable = forms.MultipleChoiceField(
        choices=[('2m_temperature', '2m Temperature')],  # Append additional variables as required
        initial=['2m_temperature'],
        label='Variables(s)',
        widget=forms.CheckboxSelectMultiple
    )

    year = forms.MultipleChoiceField(
        choices=[(str(y), str(y)) for y in range(1940, 2027)],
        initial=['2024'],
        label='Year(s)',
        widget=forms.CheckboxSelectMultiple
    )

    month = forms.MultipleChoiceField(
        choices=[(f"{m:02d}", f"{m:02d}") for m in range(1, 13)],
        initial=['03'],
        label='Month(s)',
        widget=forms.CheckboxSelectMultiple
    )

    day = forms.MultipleChoiceField(
        choices=[(f"{d:02d}", f"{d:02d}") for d in range(1, 32)],
        initial=['01'],
        label='Day(s)',
        widget=forms.CheckboxSelectMultiple
    )

    time = forms.MultipleChoiceField(
        choices=[(f"{h:02d}:00", f"{h:02d}:00") for h in range(24)],
        initial=['13:00'],
        label='Time(s)',
        widget=forms.CheckboxSelectMultiple
    )

    area = forms.CharField(
        initial='30, 70, 8, 90',
        help_text="Format: North, West, South, East (e.g., 30, 70, 8, 90)",
        label='Bounding Box'
    )

    data_format = forms.ChoiceField(
        choices=[('grib', 'GRIB'), ('netcdf', 'NetCDF')],
        initial='grib',
        label='Data Format'
    )

    download_format = forms.ChoiceField(
        choices=[('unarchived', 'Unarchived'), ('zip', 'ZIP')],
        initial='unarchived',
        label='Download Format'
    )

class EarthEngineForm(forms.Form):
    """Specific parameters for Google Earth Engine."""
    asset_id = forms.CharField(max_length=255)
    bbox = forms.CharField(help_text="Bounding box coordinates: min_lon, min_lat, max_lon, max_lat")

# Subclass forms for Hugging Face, NASA, NOAA, OWID, and World Bank respectively.