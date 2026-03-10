# zipcode features

similar to [uszipcode-project](https://github.com/EricSchles/uszipcode-project)

## Getting CBSA mapping

If you need CBSA data you can append it to the dataframe with the following example:

```python
def _get_cbsa_data():
    return pd.read_excel(
        "https://github.com/EricSchles/zipcode_features/blob/main/zipcode_features/CBSA_ZIP_122025.xlsx",
        sheet_name='Export Worksheet'
    )[["CBSA", "ZIP"]]

demo = us_get_demographics(state="NY")
cbsa_zip_map = _get_cbsa_data()
df = pd.merge(demo, cbsa_zip_map, how="left", left_on="zipcode", right_on="ZIP")
```

