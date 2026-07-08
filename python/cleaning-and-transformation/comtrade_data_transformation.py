
# Clean Comtrade Data Notebook
# This notebook cleans the raw UN Comtrade bilateral exports dataset and creates an analytics-ready Comtrade file. Note : This notebook does not modify or delete your raw Comtrade files.



# Import necessary libraries
import os
from datetime import datetime
import numpy as np
import pandas as pd



# Define file paths for raw and processed data
RAW_COMTRADE_FILE = r"C:\Users\hp\OneDrive\Desktop\global-trade-supply-chain-intelligence\data\raw_data\comtrade_data\world_bilateral_exports_final_total_2015_2024_20260706_031419.csv"
PROCESSED_OUTPUT_DIR = r"C:\Users\hp\OneDrive\Desktop\global-trade-supply-chain-intelligence\data\processed_data"

os.makedirs(PROCESSED_OUTPUT_DIR, exist_ok=True)

# print("Raw file path:")
# print(RAW_COMTRADE_FILE)
# print("Processed output folder:")
# print(PROCESSED_OUTPUT_DIR)



# Loading the raw dataset
df_raw = pd.read_csv(RAW_COMTRADE_FILE)

# print("Raw dataset loaded successfully.")
# print(f"Rows: {df_raw.shape[0]:,}")
# print(f"Columns: {df_raw.shape[1]:,}")

df_raw.head()


# Understanding the raw dataset structure
# Listing all the columns in the raw dataset
df_raw.columns.tolist()
['typecode',
 'freqcode',
 'refperiodid',
 'refyear',
 'refmonth',
 'period',
 'reportercode',
 'reporteriso',
 'reporterdesc',
 'flowcode',
 'flowdesc',
 'partnercode',
 'partneriso',
 'partnerdesc',
 'partner2code',
 'partner2iso',
 'partner2desc',
 'classificationcode',
 'classificationsearchcode',
 'isoriginalclassification',
 'cmdcode',
 'cmddesc',
 'aggrlevel',
 'isleaf',
 'customscode',
 'customsdesc',
 'moscode',
 'motcode',
 'motdesc',
 'qtyunitcode',
 'qtyunitabbr',
 'qty',
 'isqtyestimated',
 'altqtyunitcode',
 'altqtyunitabbr',
 'altqty',
 'isaltqtyestimated',
 'netwgt',
 'isnetwgtestimated',
 'grosswgt',
 'isgrosswgtestimated',
 'cifvalue',
 'fobvalue',
 'primaryvalue',
 'legacyestimationflag',
 'isreported',
 'isaggregate',
 'download_year',
 'reporter_batch_number',
 'download_timestamp']

# Checking info of the raw dataset
df_raw.info()



# Getting summary statistics of the raw dataset
df_raw.describe(include="all").T



# Checking for duplicate rows in the raw dataset
duplicate_rows = df_raw.duplicated().sum()
print(f"No of duplicate rows in raw dataset: {duplicate_rows:,}")



# Checking for missing values and their percentage in the raw dataset
missing_summary = pd.DataFrame({
    "missing_count": df_raw.isna().sum(),
    "missing_pct": (df_raw.isna().mean() * 100).round(2)
}).sort_values("missing_pct", ascending=False)



# Standardizing column names for better readability
column_rename_map = {
    "typecode": "type_code",
    "freqcode": "freq_code",
    "refperiodid": "ref_period_id",
    "refyear": "reference_year",
    "refmonth": "reference_month",
    "period": "period",
    "reportercode": "reporter_code",
    "reporteriso": "reporter_iso3",
    "reporterdesc": "reporter_name",
    "flowcode": "flow_code",
    "flowdesc": "flow_name",
    "partnercode": "partner_code",
    "partneriso": "partner_iso3",
    "partnerdesc": "partner_name",
    "partner2code": "partner_2_code",
    "partner2iso": "partner_2_iso3",
    "partner2desc": "partner_2_name",
    "classificationcode": "classification_revision_code",
    "classificationsearchcode": "classification_search_code",
    "isoriginalclassification": "is_original_classification",
    "cmdcode": "commodity_code",
    "cmddesc": "commodity_description",
    "aggrlevel": "aggregation_level",
    "isleaf": "is_leaf",
    "customscode": "customs_code",
    "customsdesc": "customs_description",
    "moscode": "mode_of_supply_code",
    "motcode": "mode_of_transport_code",
    "motdesc": "mode_of_transport_description",
    "qtyunitcode": "quantity_unit_code",
    "qtyunitabbr": "quantity_unit_abbreviation",
    "qty": "quantity",
    "isqtyestimated": "is_quantity_estimated",
    "altqtyunitcode": "alternate_quantity_unit_code",
    "altqtyunitabbr": "alternate_quantity_unit_abbreviation",
    "altqty": "alternate_quantity",
    "isaltqtyestimated": "is_alternate_quantity_estimated",
    "netwgt": "net_weight_kg",
    "isnetwgtestimated": "is_net_weight_estimated",
    "grosswgt": "gross_weight_kg",
    "isgrosswgtestimated": "is_gross_weight_estimated",
    "cifvalue": "cif_value_usd",
    "fobvalue": "fob_value_usd",
    "primaryvalue": "trade_value_usd",
    "legacyestimationflag": "legacy_estimation_flag",
    "isreported": "is_reported",
    "isaggregate": "is_aggregate",
    "download_year": "download_year",
    "reporter_batch_number": "reporter_batch_number",
    "download_timestamp": "download_timestamp"
}

df = df_raw.rename(columns=column_rename_map).copy()

print(f"Total columns after renaming: {len(df.columns)}")



# Checking the new column names after renaming
df.columns.tolist()
['type_code',
 'freq_code',
 'ref_period_id',
 'reference_year',
 'reference_month',
 'period',
 'reporter_code',
 'reporter_iso3',
 'reporter_name',
 'flow_code',
 'flow_name',
 'partner_code',
 'partner_iso3',
 'partner_name',
 'partner_2_code',
 'partner_2_iso3',
 'partner_2_name',
 'classification_revision_code',
 'classification_search_code',
 'is_original_classification',
 'commodity_code',
 'commodity_description',
 'aggregation_level',
 'is_leaf',
 'customs_code',
 'customs_description',
 'mode_of_supply_code',
 'mode_of_transport_code',
 'mode_of_transport_description',
 'quantity_unit_code',
 'quantity_unit_abbreviation',
 'quantity',
 'is_quantity_estimated',
 'alternate_quantity_unit_code',
 'alternate_quantity_unit_abbreviation',
 'alternate_quantity',
 'is_alternate_quantity_estimated',
 'net_weight_kg',
 'is_net_weight_estimated',
 'gross_weight_kg',
 'is_gross_weight_estimated',
 'cif_value_usd',
 'fob_value_usd',
 'trade_value_usd',
 'legacy_estimation_flag',
 'is_reported',
 'is_aggregate',
 'download_year',
 'reporter_batch_number',
 'download_timestamp']



# Inspect important business columns
# Displaying value counts for selected columns to understand their distribution
for col in ["type_code", "freq_code", "flow_code", "flow_name", "commodity_code", "commodity_description"]:
    print(f"\nValue counts for {col}:")
    print(df[col].value_counts(dropna=False).head(20))

print("Reference years present in dataset:")
print(sorted(df["reference_year"].dropna().unique().tolist()))

print("Classification revision codes present:")
print(sorted(df["classification_revision_code"].dropna().unique().tolist()))



# Deciding which columns should be kept for the analytics-ready file
columns_to_keep = [
    "reference_year",
    "period",
    "reporter_code",
    "reporter_iso3",
    "reporter_name",
    "partner_code",
    "partner_iso3",
    "partner_name",
    "trade_value_usd",
    "fob_value_usd",
    "flow_code",
    "flow_name",
    "commodity_code",
    "commodity_description",
    "type_code",
    "freq_code",
    "classification_revision_code",
    "is_reported",
    "is_aggregate",
    "download_timestamp"
]

df_clean = df[columns_to_keep].copy()

print(f"Rows: {df_clean.shape[0]:,}")
print(f"Columns kept: {df_clean.shape[1]}")

df_clean.head()



# Converting data types for better analysis and storage efficiency
numeric_int_cols = [
    "reference_year",
    "period",
    "reporter_code",
    "partner_code"
]

for col in numeric_int_cols:
    df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce").astype("Int64")

numeric_value_cols = [
    "trade_value_usd",
    "fob_value_usd"
]

for col in numeric_value_cols:
    df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")

flag_cols = ["is_reported", "is_aggregate"]

for col in flag_cols:
    df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce").astype("Int64")

df_clean["download_timestamp"] = pd.to_datetime(
    df_clean["download_timestamp"],
    errors="coerce",
    dayfirst=True
)

string_cols = [
    "reporter_iso3", "reporter_name",
    "partner_iso3", "partner_name",
    "flow_code", "flow_name",
    "commodity_code", "commodity_description",
    "type_code", "freq_code",
    "classification_revision_code"
]

for col in string_cols:
    df_clean[col] = df_clean[col].astype("string").str.strip()

print("Data type conversion completed.")

df_clean.info()

# Add a World partner flag
# Rows where partner_iso3 = 'W00' represent reporter-to-world totals rather than bilateral partner rows. This flag makes those rows easier to identify later.
df_clean["is_world_partner"] = pd.Series(
    np.where(df_clean["partner_iso3"] == "W00", 1, 0),
    index=df_clean.index
).astype("Int64")

df_clean["is_world_partner"].value_counts(dropna=False)



# Checking for missing values and their percentage in the cleaned dataset
clean_missing_summary = pd.DataFrame({
    "missing_count": df_clean.isna().sum(),
    "missing_pct": (df_clean.isna().mean() * 100).round(2)
}).sort_values("missing_pct", ascending=False)

clean_missing_summary



# Checking for duplicate rows based on business key columns
business_key_cols = [
    "reference_year",
    "reporter_code",
    "partner_code",
    "commodity_code",
    "flow_code"
]

duplicate_business_rows = df_clean.duplicated(subset=business_key_cols).sum()

print("Duplicate rows based on business key:")
print(duplicate_business_rows)


# Basic data quality checks
negative_trade_rows = (df_clean["trade_value_usd"] < 0).sum()
print(f"Rows with negative trade values: {negative_trade_rows:,}")

print("\nReference year min / max:")
print(df_clean["reference_year"].min(), df_clean["reference_year"].max())

print("\nFlow code distribution:")
print(df_clean["flow_code"].value_counts(dropna=False))

print("\nCommodity code distribution:")
print(df_clean["commodity_code"].value_counts(dropna=False))




# Setting final column order for the analytics-ready dataset
final_column_order = [
    "reference_year",
    "period",
    "reporter_code",
    "reporter_iso3",
    "reporter_name",
    "partner_code",
    "partner_iso3",
    "partner_name",
    "is_world_partner",
    "trade_value_usd",
    "fob_value_usd",
    "flow_code",
    "flow_name",
    "commodity_code",
    "commodity_description",
    "type_code",
    "freq_code",
    "classification_revision_code",
    "is_reported",
    "is_aggregate",
    "download_timestamp"
]

df_final = df_clean[final_column_order].copy()
df_final.head()


# Saving the final cleaned Comtrade dataset
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

output_file_name = f"comtrade_exports_clean_analytics_ready_{timestamp}.csv"
output_file_path = os.path.join(PROCESSED_OUTPUT_DIR, output_file_name)

df_final.to_csv(output_file_path, index=False)

print("Cleaned Comtrade analytics-ready file saved successfully.")
print(output_file_path)

# Final summary of the cleaned output
print("----CLEANED COMTRADE DATA SUMMARY----")
print(f"Rows: {df_final.shape[0]:,}")
print(f"Columns: {df_final.shape[1]:,}")
print(f"Reference year range: {df_final['reference_year'].min()} to {df_final['reference_year'].max()}")
print(f"World-partner rows: {df_final['is_world_partner'].sum():,}")
print(f"Cleaned output file: {output_file_path}")