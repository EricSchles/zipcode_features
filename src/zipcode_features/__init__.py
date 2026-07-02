__version__ = '0.0.7'

import zipcodes
from zipcode3.search import SearchEngine
from importlib import resources
import pandas as pd
import json

def zipcode_mapper(x):
    if x["ZIP_len"] == 3: 
        return "00" + x["ZIP"]
    elif x["ZIP_len"] == 4: 
        return "0" + x["ZIP"]
    else:
        return x["ZIP"]
    
def _get_zip_to_cbsa_code() -> dict:
    """
    This method gets a mapping from zipcode to cbsa code
    mapping is of the form:
    {"zip code": "cbsa code"}
    """
    with resources.path("zipcode_features.data", "CBSA_ZIP_122025.csv") as csv_path:
        df = pd.read_csv(csv_path, dtype={'ZIP': str, "CBSA": str})
    df["ZIP_len"] = df["ZIP"].apply(lambda x: len(x))
    df["ZIP"] = df.apply(zipcode_mapper, axis=1)
    return df[["ZIP", "CBSA"]].to_dict()

def _get_cbsa_code_to_cbsa_name() -> dict:
    """
    This method gets a mapping from cbsa code to name
    {cbsa code: cbsa name}
    """
    with resources.path("zipcode_features.data", "cbsa_codes.json") as json_path:
        code_to_name = json.load(open(json_path))
    df = pd.DataFrame(columns=["code", "name"])
    df["name"] = code_to_name.values()
    df["code"] = code_to_name.keys()
    df["name"] = df["name"].str.replace(" -", "-")
    df["name"] = df["name"].str.split().str.join(' ')
    return df.to_dict()

    
def us_get_demographics(state: str, city: str = None, zip_list: list = None) -> pd.DataFrame:
    """
    This gets demographic information for associated with zipcodes in the United States of America.

    Parameters
    ----------
    * state : str - the US state
    * city : str [Optional] - the US city
    * zip_list : list [Optional] - a zip list is the query results from the zipcodes library.
    Found here: https://github.com/seanpianka/zipcodes
    If you use zip_list state and city will be ignored.

    Returns
    -------
    A pandas dataframe with zipcode and everything typically returned by
    https://github.com/EricSchles/uszipcode-project
    """
    search = SearchEngine()
    if city is None:
        payload = {
            "state": state
        }
    else:
        payload = {
            "state": state,
            "city": city
        }
    if zip_list is None:
        zipcode_and_demo = [
            [zipcode["zip_code"], search.by_zipcode(zipcode["zip_code"])]
            for zipcode in zipcodes.filter_by(**payload)
        ]
    else:
        zipcode_and_demo = zip_list[:]
    demographics = []
    for info in zipcode_and_demo:
        if info[1] is None:
            continue
        tmp_dict = info[1].to_dict()
        tmp_dict["zip_code"] = info[0]
        demographics.append(tmp_dict)
    df = pd.DataFrame(demographics)
    zip_to_cbsa = _get_zip_to_cbsa_code()
    df["cbsa"] = df["zip_code"].map(zip_to_cbsa)
    cbsa_code_to_name = _get_cbsa_code_to_cbsa_name()
    df["cbsa_name"] = df["cbsa"].map(cbsa_code_to_name)
    return df
    
