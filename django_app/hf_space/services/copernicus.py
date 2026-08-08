import cdsapi, os
import xarray as xr
from dotenv import load_dotenv, find_dotenv
from django.conf import settings

load_dotenv(find_dotenv())

class CopernicusService:
    def __init__(self):
        # url, key are saved to .cdsapirc
        self.client = cdsapi.Client(os.getenv('CDSAPI_URL'), os.getenv('CDSAPI_KEY'))

    def fetch_data(self, cleaned_data: dict) -> list:
        """
        Submits the parameterized query to the CDS API, downloads the asset,
        and initiates the parsing sequence.
        """
        # Isolate the dataset identifier from the payload parameters
        dataset = cleaned_data.pop('dataset')

        # Enforce numerical list format for spatial boundaries
        if 'area' in cleaned_data:
            raw_area = cleaned_data['area']

            # Extract the string if it was improperly wrapped in a single-element list
            if isinstance(raw_area, list) and isinstance(raw_area[0], str):
                raw_area = raw_area[0]

            # Cast the comma-separated string into a list of numerical coordinates
            if isinstance(raw_area, str):
                cleaned_data['area'] = [float(coord.strip()) for coord in raw_area.split(',')]

        # Define a temporary file path for the binary download
        file_path = os.path.join(settings.BASE_DIR, 'temp_copernicus_output.grib')

        # Execute API request with corrected payload
        self.client.retrieve(dataset, cleaned_data, file_path)

        return self._parse_grib_to_tabular(file_path)

    @staticmethod
    def _parse_grib_to_tabular(file_path: str) -> list:
        try:
            # Decode the GRIB binary into an xarray Dataset
            dataset = xr.open_dataset(file_path, engine='cfgrib')

            # Transform the dimensional matrix into a 2D Pandas DataFrame
            dataframe = dataset.to_dataframe().reset_index()
            dataset.close()

            # Serialize a subset of the DataFrame to prevent HTTP payload saturation
            records = dataframe.head(100).to_dict(orient='records')
            return records

        finally:
            # Ensure deterministic cleanup of the temporary binary asset
            if os.path.exists(file_path):
                os.remove(file_path)