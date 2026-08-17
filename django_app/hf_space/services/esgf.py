import requests


class ESGFService:
    def fetch_data(self, dataset_id: str, cleaned_data: dict) -> list:
        experiment = cleaned_data.get("experiment", "historical")
        variable = cleaned_data.get("variable", "tas")

        # Query the LLNL ESGF Search API for CMIP6 projections
        url = "https://esgf-node.llnl.gov/esg-search/search"
        params = {"project": "CMIP6", "experiment_id": experiment, "variable_id": variable,
                  "format": "application/solr+json", "limit": 25, "type": "Dataset"}
        try:
            resp = requests.get(url, params=params)
            if resp.status_code == 200:
                docs = resp.json().get("response", {}).get("docs", [])
                results = [
                    {"Dataset ID": d.get("instance_id", "N/A"), "Institution": d.get("institution_id", ["N/A"])[0],
                     "Model": d.get("source_id", ["N/A"])[0], "Grid": d.get("grid_label", ["N/A"])[0]} for d in docs]
                return results if results else [{"Status": "No CMIP6 datasets found for these parameters."}]
            return [{"Error": f"ESGF API Error {resp.status_code}"}]
        except Exception as e:
            return [{"Processing Error": str(e)}]