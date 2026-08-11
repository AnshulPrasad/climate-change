import requests
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

class NOAAService:
    def __init__(self):
        pass

    def temp(self):
        NOAA_TOKEN: str = os.getenv("NOAA_TOKEN")
        headers = {"token": NOAA_TOKEN}

        # Endpoint for fetching observational data
        endpoint = "https://www.ncei.noaa.gov/cdo-web/api/v2/data"

        params = {
            "datasetid": "GSOM",  # Global Summary of the Month
            "stationid": "GHCND:USW00023234",  # Specific station
            # "locationid": "FIPS:06",  # California
            "startdate": "2023-01-01",
            "enddate": "2023-01-31",
            "limit": 1000,
        }

        response = requests.get(endpoint, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            print("Success:", data.get("results", [])[:2])
        else:
            print(f"HTTP Error {response.status_code}: {response.text}")