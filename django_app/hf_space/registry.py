from .forms.copernicus import DynamicCDSFormFactory
from .forms.earth_engine import EarthEngineFormFactory
from .services.copernicus import CopernicusService
from .services.earth_engine import EarthEngineService

PROVIDER_REGISTRY = {
    'copernicus': {
        'name': 'Copernicus Climate Data Store',
        'form_class': DynamicCDSFormFactory.create_form,
        'service_class': CopernicusService,
        'template_name': 'hf_space/providers/copernicus_dashboard.html', # Dedicated template
        'datasets': {
            'reanalysis-era5-single-levels': 'ERA5 Single Levels',
            'reanalysis-era5-pressure-levels': 'ERA5 Pressure Levels',
            'ecv-for-climate-change': 'Essential Climate Variables (1979-Present)'
        }
    },
    'earth_engine': {
        'name': 'Google Earth Engine',
        'form_class': EarthEngineFormFactory.create_form,
        'service_class': EarthEngineService,
        'template_name': 'hf_space/providers/earth_engine_dashboard.html', # Dedicated template
        'datasets': {
            'sentinel-5p': 'Sentinel-5P (Atmospheric Composition)',
            'hansen-global-forest-change': 'Hansen Global Forest Change',
            'modis-land-surface-temp': 'MODIS Land Surface Temperature',
            'jrc-global-surface-water': 'JRC Global Surface Water'
        }
    }
}