# zipcode features

similar to [uszipcode-project](https://github.com/EricSchles/uszipcode-project)

## Getting CBSA mapping

If you need CBSA data you can append it to the dataframe with the following example:

```python
from zipcode_features import us_get_demographics
import pandas as pd

def _get_cbsa_data():
    return pd.read_excel(
        "https://github.com/EricSchles/zipcode_features/blob/main/zipcode_features/CBSA_ZIP_122025.xlsx",
        sheet_name='Export Worksheet'
    )[["CBSA", "ZIP"]]

demo = us_get_demographics(state="NY")
cbsa_zip_map = _get_cbsa_data()
df = pd.merge(demo, cbsa_zip_map, how="left", left_on="zipcode", right_on="ZIP")
```

For the semantic names you can get them [here](https://www2.census.gov/programs-surveys/cps/methodology/2015%20Geography%20Cover.pdf).

Here's a python script to parse them:

```python
import urllib.request
import PyPDF2
import json
import re
import io

def fetch_cbsa_to_json():
    url = "https://www2.census.gov/programs-surveys/cps/methodology/2015%20Geography%20Cover.pdf"
    
    print("Downloading Census PDF...")
    # Using a User-Agent to ensure the request isn't blocked by the server
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        response = urllib.request.urlopen(req)
        pdf_bytes = io.BytesIO(response.read())
    except Exception as e:
        print(f"Failed to download PDF: {e}")
        return

    print("Parsing PDF...")
    reader = PyPDF2.PdfReader(pdf_bytes)
    
    cbsa_mapping = {}
    
    # Regular expression to match a 5-digit FIPS/CBSA code followed by the area name
    # Example match: "11460 Ann Arbor, MI"
    pattern = re.compile(r'\b(\d{5})\s+(.+?)(?=\s+\d{5}|\n|$)')
    
    for page in reader.pages:
        text = page.extract_text()
        if text:
            matches = pattern.findall(text)
            for code, name in matches:
                # Clean up any trailing spaces or artifacts
                clean_name = name.strip()
                # Exclude standalone numbers or random headers that might get caught
                if len(clean_name) > 2 and not clean_name.isdigit():
                    cbsa_mapping[code] = clean_name
                    
    print(f"Extracted {len(cbsa_mapping)} CBSA codes.")
    
    # Save the mapping to a JSON file
    output_file = 'cbsa_codes.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cbsa_mapping, f, indent=4)
        
    print(f"Successfully saved to {output_file}")

if __name__ == "__main__":
    fetch_cbsa_to_json()
```

Here's a working example for using this with the above:

```python
import requests
from zipcode_features import us_get_demographics
import pandas as pd

def _get_cbsa_data():
    return pd.read_excel(
        "https://github.com/EricSchles/zipcode_features/blob/main/zipcode_features/CBSA_ZIP_122025.xlsx",
        sheet_name='Export Worksheet'
    )[["CBSA", "ZIP"]]

demo = us_get_demographics(state="NY")
cbsa_zip_map = _get_cbsa_data()
df = pd.merge(demo, cbsa_zip_map, how="left", left_on="zipcode", right_on="ZIP")
df = df.drop("ZIP", axis=1)
mapping = requests.get("https://raw.githubusercontent.com/EricSchles/zipcode_features/refs/heads/main/zipcode_features/cbsa_codes.json").json()
df["cbsa_name"] = df["CBSA"].map(mapping)
df = df.drop("CBSA", axis=1)
```