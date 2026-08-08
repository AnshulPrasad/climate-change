from django.shortcuts import render
from .forms import CopernicusForm, EarthEngineForm
from django.http import HttpResponseBadRequest
from .services.copernicus import CopernicusService

# Registry mapping service identifiers to their respective forms
FORM_REGISTRY = {
    'copernicus': CopernicusForm,
    'earth_engine': EarthEngineForm,
}

# Registry mapping service identifiers to output formats
OUTPUT_FORMAT_REGISTRY = {
    'copernicus': 'tabular',
    'earth_engine': 'raster',
}

# Create your views here.
def dashboard(request, service_name='copernicus'):
    """Dynamically initializes form and processes data based on service selection."""
    if service_name not in FORM_REGISTRY:
        return HttpResponseBadRequest("Invalid service specified.")

    form_class = FORM_REGISTRY.get(service_name, 'copernicus')
    output_format = OUTPUT_FORMAT_REGISTRY.get(service_name, 'tabular')
    output_data = None

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            # Route validated data to the respective service execution handler
            if service_name == 'copernicus':
                service = CopernicusService()
                output_data = service.fetch_data(form.cleaned_data)
            # Add elif blocks for additional services here
    else:
        form = form_class()
    context = {
        'form': form,
        'service_name': service_name,
        'output_data': output_data,
        'output_format':output_format
    }

    return render(request, 'core/dashboard.html', context)