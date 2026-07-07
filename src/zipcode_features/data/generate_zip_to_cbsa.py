from glob import glob
import pandas as pd
import json

def generate_final_cbsa_to_zip():
    df = pd.read_csv("CBSA_ZIP_122025.csv")
    df = df[["ZIP", "CBSA"]]
    for data in glob("*ZIP-CBSA*"):
        tmp = pd.read_csv(data)
        diff = tmp[~tmp["zip"].isin(df["ZIP"])]
        diff["ZIP"] = diff["zip"]
        diff["CBSA"] = diff["geoid"]
        diff.drop("zip", axis=1, inplace=True)
        diff.drop("geoid", axis=1, inplace=True)
        df = pd.concat([df, diff])

    df.to_csv("cbsa_to_zip.csv")

def generate_final_cbsa_codes():
    cbsa_codes = json.load(open("cbsa_codes.json", "r"))
    cbsa = pd.Series(cbsa_codes.keys())
    for data in glob("cbsa_codes*.json"):
        tmp_cbsa_codes = json.load(open(data, "r"))
        tmp_cbsa = pd.Series(tmp_cbsa_codes.keys())
        not_in_orig = tmp_cbsa[~tmp_cbsa.isin(cbsa)]
        tmp_dict = {code: tmp_cbsa_codes[code] for code in not_in_orig}
        cbsa_codes.update(tmp_dict)

    json.dump(cbsa_codes, open("cbsa_codes_bigger.json", "w"))


