__version__ = '0.0.9'

import zipcodes
from zipcode3.search import SearchEngine
from importlib import resources
import pandas as pd
import json
from functools import partial

zip_to_fips = {
    '00544': '36103', # Suffolk County
    '10015': '36061', # New York County (Manhattan)
    '10046': '36061', # New York County
    '10047': '36061', # New York County
    '10048': '36061', # New York County
    '10060': '36061', # New York County
    '10072': '36061', # New York County
    '10079': '36061', # New York County
    '10082': '36061', # New York County
    '10087': '36061', # New York County
    '10090': '36061', # New York County
    '10094': '36061', # New York County
    '10095': '36061', # New York County
    '10096': '36061', # New York County
    '10098': '36061', # New York County
    '10099': '36061', # New York County
    '10102': '36061', # New York County
    '10109': '36061', # New York County
    '10114': '36061', # New York County
    '10130': '36061', # New York County
    '10132': '36061', # New York County
    '10149': '36061', # New York County
    '10161': '36061', # New York County
    '10184': '36061', # New York County
    '10196': '36061', # New York County
    '10197': '36061', # New York County
    '10200': '36061', # New York County
    '10242': '36061', # New York County
    '10249': '36061', # New York County
    '10256': '36061', # New York County
    '10257': '36061', # New York County
    '10259': '36061', # New York County
    '10260': '36061', # New York County
    '10261': '36061', # New York County
    '10265': '36061', # New York County
    '10270': '36061', # New York County
    '10273': '36061', # New York County
    '10286': '36061', # New York County
    '10292': '36061', # New York County
    '10499': '36005', # Bronx County
    '10521': '36119', # Westchester County
    '10557': '36119', # Westchester County
    '10558': '36119', # Westchester County
    '10571': '36119', # Westchester County
    '10572': '36119', # Westchester County
    '10943': '36071', # Orange County
    '10997': '36071', # Orange County
    '11025': '36059', # Nassau County
    '11026': '36059', # Nassau County
    '11027': '36059', # Nassau County
    '11041': '36059', # Nassau County
    '11043': '36059', # Nassau County
    '11044': '36059', # Nassau County
    '11051': '36059', # Nassau County
    '11052': '36059', # Nassau County
    '11053': '36059', # Nassau County
    '11054': '36059', # Nassau County
    '11055': '36059', # Nassau County
    '11099': '36059', # Nassau County
    '11120': '36081', # Queens County
    '11240': '36047', # Kings County (Brooklyn)
    '11244': '36047', # Kings County
    '11248': '36047', # Kings County
    '11254': '36047', # Kings County
    '11255': '36047', # Kings County
    '11381': '36081', # Queens County
    '11390': '36081', # Queens County
    '11535': '36059', # Nassau County
    '11536': '36059', # Nassau County
    '11555': '36059', # Nassau County
    '11592': '36059', # Nassau County
    '11594': '36059', # Nassau County
    '11595': '36059', # Nassau County
    '11597': '36059', # Nassau County
    '11690': '36081', # Queens County
    '11695': '36081', # Queens County
    '11707': '36103', # Suffolk County
    '11708': '36103', # Suffolk County
    '11736': '36103', # Suffolk County
    '11737': '36103', # Suffolk County
    '11750': '36103', # Suffolk County
    '11760': '36103', # Suffolk County
    '11774': '36059', # Nassau County
    '11775': '36059', # Nassau County
    '11819': '36059', # Nassau County
    '11853': '36059', # Nassau County
    '11854': '36059', # Nassau County
    '11855': '36059', # Nassau County
    '12016': '36057', # Montgomery County
    '12214': '36001', # Albany County
    '12225': '36001', # Albany County
    '12228': '36001', # Albany County
    '12229': '36001', # Albany County
    '12230': '36001', # Albany County
    '12231': '36001', # Albany County
    '12238': '36001', # Albany County
    '12241': '36001', # Albany County
    '12242': '36001', # Albany County
    '12243': '36001', # Albany County
    '12244': '36001', # Albany County
    '12250': '36001', # Albany County
    '12252': '36001', # Albany County
    '12256': '36001', # Albany County
    '12261': '36001', # Albany County
    '12325': '36093', # Schenectady County
    '12593': '36027', # Dutchess County
    '12727': '36105', # Sullivan County
    '13056': '36053', # Madison County
    '13107': '36075', # Oswego County
    '13221': '36067', # Onondaga County
    '13250': '36067', # Onondaga County
    '13251': '36067', # Onondaga County
    '13449': '36065', # Oneida County
    '13465': '36065', # Oneida County
    '13599': '36065', # Oneida County
    '13627': '36045', # Jefferson County
    '13657': '36049', # Lewis County
    '13763': '36025', # Delaware County
    '13837': '36025', # Delaware County
    '14133': '36063', # Niagara County
    '14261': '36029', # Erie County
    '14264': '36029', # Erie County
    '14267': '36029', # Erie County
    '14443': '36069', # Ontario County
    '14644': '36055', # Monroe County
    '14645': '36055', # Monroe County
    '14650': '36055', # Monroe County
    '14664': '36055', # Monroe County
    '14673': '36055', # Monroe County
    '14683': '36055', # Monroe County
    '14694': '36055', # Monroe County
    '14756': '36013', # Chautauqua County
    '14925': '36015', # Chemung County
}

def code_mapper(col, x):
    if x[f"{col}_len"] == 2:
        return "000" + x[col]
    if x[f"{col}_len"] == 3: 
        return "00" + x[col]
    elif x[f"{col}_len"] == 4: 
        return "0" + x[col]
    else:
        return x[col]

def map_zip_to_cbsa(zip_to_cbsa, zip_code):
    if zip_code in zip_to_cbsa:
        return zip_to_cbsa[zip_code]
    else:
        return '00000'

def _get_zip_to_cbsa_code() -> dict:
    """
    This method gets a mapping from zipcode to cbsa code
    mapping is of the form:
    {"zip code": "cbsa code"}
    """
    with resources.path("zipcode_features.data", "CBSA_ZIP_122025.csv") as csv_path:
        df = pd.read_csv(csv_path, dtype={'ZIP': str, "CBSA": str})
    df = correct_code(df, "ZIP")
    mapping = df.set_index('ZIP')['CBSA'].to_dict()
    return partial(map_zip_to_cbsa, mapping)

def map_cbsa_code_to_name(cbsa_code_to_name, cbsa_code):
    if cbsa_code in cbsa_code_to_name:
        return cbsa_code_to_name[cbsa_code]
    else:
        return 'Unknown'

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
    code_to_name = df.set_index('code')['name'].to_dict()
    return partial(map_cbsa_code_to_name, code_to_name)

def correct_code(df: pd.DataFrame, col: str) -> pd.DataFrame:
    df[f"{col}_len"] = df[col].apply(lambda x: len(x))
    corrector = partial(code_mapper, col)
    df[col] = df.apply(corrector, axis=1)
    return df

def map_zip_code_to_fips_code(zip_code_to_fips_code, zip_code):
    if zip_code in zip_code_to_fips_code:
        return zip_code_to_fips_code[zip_code]
    else:
        return '000000'
    #fips codes are 5 digits long, so this should always
    #map to nothing

def _get_zip_to_fips_code() -> dict:
    with resources.path("zipcode_features.data", "ZIP_COUNTY_122025.csv") as csv_path:
        df = pd.read_csv(csv_path, dtype={'ZIP': str, "COUNTY": str})

    df = correct_code(df, "ZIP")
    df = correct_code(df, "COUNTY")
    df = df[["ZIP", "COUNTY"]]
    zip_to_county = df.set_index('ZIP')['COUNTY'].to_dict()
    zip_to_county.update(zip_to_fips)
    return partial(map_zip_code_to_fips_code, zip_to_county)
    
def _get_bls_data() -> pd.DataFrame:
    csvs = [
        "bls_2025_quarter_four.csv",
        "bls_2025_quarter_one.csv",
        "bls_2025_quarter_three.csv", 
        "bls_2025_quarter_two.csv"
    ]
    cols_to_drop = [
        "own_code",
        "industry_code",
        "agglvl_code",
        "size_code",
        "disclosure_code",
        'lq_disclosure_code',
        'lq_qtrly_estabs',
        'lq_month1_emplvl',
        'lq_month2_emplvl',
        'lq_month3_emplvl',
        'lq_total_qtrly_wages',
        'lq_taxable_qtrly_wages',
        'lq_qtrly_contributions',
        'lq_avg_wkly_wage',
        'oty_disclosure_code',
        'oty_qtrly_estabs_chg',
        'oty_qtrly_estabs_pct_chg',
        'oty_month1_emplvl_chg',
        'oty_month1_emplvl_pct_chg',
        'oty_month2_emplvl_chg',
        'oty_month2_emplvl_pct_chg',
        'oty_month3_emplvl_chg',
        'oty_month3_emplvl_pct_chg',
        'oty_total_qtrly_wages_chg',
        'oty_total_qtrly_wages_pct_chg',
        'oty_taxable_qtrly_wages_chg',
        'oty_taxable_qtrly_wages_pct_chg',
        'oty_qtrly_contributions_chg',
        'oty_qtrly_contributions_pct_chg',
        'oty_avg_wkly_wage_chg',
        'oty_avg_wkly_wage_pct_chg'
    ]
    final_df = pd.DataFrame()
    for csv in csvs:
        with resources.path("zipcode_features.data", csv) as csv_path:
            df = pd.read_csv(csv_path)
            df = df.drop(cols_to_drop, axis=1)
            final_df = pd.concat([final_df, df], ignore_index=True)
    final_df = final_df.rename({"area_fips": "fips_code"}, axis=1)
    final_df["fips_code"] = final_df["fips_code"].astype(str)
    return final_df

    
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
    df["cbsa"] = df["zip_code"].apply(zip_to_cbsa)
    cbsa_code_to_name = _get_cbsa_code_to_cbsa_name()
    df["cbsa_name"] = df["cbsa"].apply(cbsa_code_to_name)
    zip_code_to_fips_code = _get_zip_to_fips_code()
    df["fips_code"] = df["zip_code"].apply(zip_code_to_fips_code)
    bls_data = _get_bls_data()
    return pd.merge(df, bls_data, how="inner", on="fips_code")

    
