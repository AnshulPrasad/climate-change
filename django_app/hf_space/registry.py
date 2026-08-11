from .forms.copernicus import DynamicCDSFormFactory
from .forms.earth_engine import EarthEngineForm
from .services.copernicus import CopernicusService
from .services.earth_engine import EarthEngineService

PROVIDER_REGISTRY = {
    'copernicus': {
        'name': 'Copernicus Climate Data Store',
        'form_class': DynamicCDSFormFactory.create_form,
        'service_class': CopernicusService,
        'template_name': 'hf_space/providers/copernicus_dashboard.html', # Dedicated template
    },
    'earth_engine': {
        'name': 'Google Earth Engine',
        'form_class': EarthEngineForm,
        'service_class': EarthEngineService,
        'template_name': 'hf_space/providers/earth_engine_dashboard.html', # Dedicated template
    }
}