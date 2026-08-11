import requests

class WorldBankService:
    pass
    def temp(self):
        # Fetch historical annual temperature averages for a given country ISO code (e.g., India - IND)
        url = "https://api.worldbank.org/v2/country/IND/indicator/EN.GHG.CO2.MT.CE.AR5?format=json"
        response = requests.get(url)
        data = response.json()
        # print(data)

        # Response structure: data[0] contains metadata, data[1] contains records
        if len(data) > 1:
            indicator_data = data[1]
            print(f"Latest record: {indicator_data[0]}")
        else:
            print(data)