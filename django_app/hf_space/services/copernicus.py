import cdsapi
from pathlib import Path
import xarray as xr

class CopernicusService:
    def __init__(self):
        self.client = cdsapi.Client()

    def fetch_data(self, provider_id: str, cleaned_data: dict) -> list:
        dataset_id = "reanalysis-era5-single-levels"

        # Determine file extension based on user selection
        data_format = cleaned_data.get("format", "grib")
        file_ext = ".nc" if data_format == "netcdf" else ".grib"

        output_path = Path(f"/tmp/{dataset_id}_output{file_ext}")

        if "area" in cleaned_data and isinstance(cleaned_data["area"], str):
            cleaned_data["area"] = [float(x.strip()) for x in cleaned_data["area"].split(",")]

        # Download the file via CDS API
        self.client.retrieve(dataset_id, cleaned_data, str(output_path))

        # Parse the downloaded binary file into a tabular dictionary
        return self._parse_file_to_table(output_path, data_format)

    def _parse_file_to_table(self, file_path: Path, data_format: str) -> list:
        """Opens the binary dataset and converts a preview slice to a list of dicts."""
        try:
            # Select the appropriate backend engine
            engine = "netcdf4" if data_format == "netcdf" else "cfgrib"

            # Open the multi-dimensional dataset
            ds = xr.open_dataset(file_path, engine=engine)

            # Flatten the dimensions into a standard tabular Pandas DataFrame
            df = ds.to_dataframe().reset_index()

            # Clean up the data by removing empty spatial nodes (NaNs)
            df = df.dropna()

            # Slice the first 100 rows for UI performance
            df_subset = df.head(100)

            # Convert all timestamps and complex objects to strings for HTML serialization
            df_subset = df_subset.astype(str)

            # Return as a list of dictionaries for Django template rendering
            return df_subset.to_dict(orient='records')

        except Exception as e:
            # If parsing fails, return the error as a table row so it's visible in the UI
            return [{"Data Processing Error": f"Failed to parse {data_format.upper()} file: {str(e)}"}]