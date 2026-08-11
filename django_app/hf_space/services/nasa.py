import earthaccess
import xarray as xr

class NASAService:
    def __init__(self):
        pass

    def temp(self):
        # Authenticate against NASA Earthdata API
        earthaccess.login()  # user id and password are used

        # Query cloud-hosted datasets (e.g., Sea Surface Temperature)
        results = earthaccess.search_data(
            short_name="MUR25-JPL-L4-GLOB-v04.2",
            temporal=("2023-01-01", "2023-01-02"),
            cloud_hosted=True
        )

        # Open remote files directly as virtual xarray datasets
        files = earthaccess.open(results)
        ds = xr.open_mfdataset(files, engine='h5netcdf', chunks=None)