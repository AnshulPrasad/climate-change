import cdsapi, os
import xarray as xr
import cfgrib, folium, matplotlib.pyplot as plt
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class CopernicusService:
    def __init__(self):
        # url, key are saved to .cdsapirc
        self._client = cdsapi.Client(os.getenv('CDSAPI_URL'), os.getenv('CDSAPI_KEY'))

    def fetch_data(self, config_data: dict):
        dataset = config_data.get('dataset', 'reanalysis-era5-single-levels')
        request = {
            'product_type': config_data.get('product_type', ['reanalysis']),
            'variable': config_data.get('variable', ['2m_temperature']),
            'year': config_data.get('year', ['2024']),
            'month': config_data.get('month', ['03']),
            'day': config_data.get('day', ['01']),
            'time': config_data.get('time', ['13:00']),
            'area': config_data.get('area', [30, 70, 8, 90]),
            'data_format': config_data.get('data_format','grib'),
            'download_format': config_data.get('download_format', 'unarchived'),
        }
        target = 'copernicus.grib'

        self._client.retrieve(dataset, request, target)

        ds = xr.open_dataset(target, engine='cfgrib')

        return ds