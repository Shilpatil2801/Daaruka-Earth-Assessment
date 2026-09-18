import pandas as pd


DATA_PATH = "data/environmental_data.csv"


def load_environmental_data():

    return pd.read_csv(DATA_PATH)


def get_region_data(region):

    df = load_environmental_data()

    result = df[
        df["region"].str.lower()
        == region.lower()
    ]

    if result.empty:
        return None

    return result.iloc[0].to_dict()