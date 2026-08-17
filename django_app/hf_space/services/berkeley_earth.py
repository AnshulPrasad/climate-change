import pandas as pd
import requests
import io


class BerkeleyEarthService:
    def fetch_data(self, dataset_id: str, cleaned_data: dict) -> list:
        region = cleaned_data.get("region", "Global")

        # Updated to the new active S3 infrastructure used by Berkeley Earth
        url = f"https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/{region}/Complete_TAVG_summary.txt"

        # Add a User-Agent to prevent HTTP 403 Forbidden/Timeout drops
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        try:
            # Added a timeout to prevent the app from hanging if the server is unresponsive
            resp = requests.get(url, headers=headers, timeout=10)

            if resp.status_code != 200:
                return [{"Error": f"Failed to fetch Berkeley Earth data. HTTP Status: {resp.status_code}"}]

            # Berkeley Earth uses '%' for comments. Parse safely into Pandas.
            df = pd.read_csv(io.StringIO(resp.text), sep=r'\s+', comment='%', header=None,
                             names=["Year", "Month", "Monthly Anomaly", "Monthly Unc.", "Annual Anomaly", "Annual Unc.",
                                    "5-Year Anomaly", "5-Year Unc.", "10-Year Anomaly", "10-Year Unc.",
                                    "20-Year Anomaly", "20-Year Unc."])

            # Fetch the last 100 recorded months to prevent overloading the UI table
            df = df.dropna(subset=['Monthly Anomaly']).tail(100)
            display_df = df[['Year', 'Month', 'Monthly Anomaly', 'Monthly Unc.']].astype(str)
            return display_df.to_dict(orient='records')

        except requests.exceptions.Timeout:
            return [{"Status": "Connection to Berkeley Earth servers timed out. Please try again later."}]
        except requests.exceptions.RequestException as e:
            return [{"Status": f"Network error occurred: {str(e)}"}]
        except Exception as e:
            return [{"Processing Error": str(e)}]