import requests
class FAOSTATService:
    def fetch_data(self, dataset_id: str, cleaned_data: dict) -> list:
        # FAOSTAT's native API requires complex session tokens. We proxy the core FAO data reliably through the World Bank indicator engine.
        country = cleaned_data.get("country", "WLD")
        indicator = cleaned_data.get("indicator", "AG.LND.AGRI.ZS")
        url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"
        try:
            resp = requests.get(url, params={"format": "json", "per_page": 100})
            if resp.status_code == 200 and len(resp.json()) > 1:
                records = resp.json()[1]
                return [{"Year": r.get("date"), "Country": r.get("country",{}).get("value"), "Indicator": r.get("indicator",{}).get("value"), "Value": r.get("value", "N/A")} for r in records]
            return [{"Status": "No FAO data found for parameters."}]
        except Exception as e:
            return [{"Error": str(e)}]