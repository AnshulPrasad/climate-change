import pandas as pd

class OWIDService:
    def __init__(self):
        pass

    def temp(self):
        url = 'https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv'

        df = pd.read_csv(url)
        df.describe()