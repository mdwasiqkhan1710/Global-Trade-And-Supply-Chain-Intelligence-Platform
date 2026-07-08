# -------------------------------------Clean World Bank Data Notebook-------------------------------------
# This notebook cleans the raw World Bank country-year dataset and creates a processed, analytics-ready World Bank file.


# Import necessary libraries
import os
from datetime import datetime
import numpy as np
import pandas as pd



# Creating variable for file paths and output directories.
RAW_WORLD_BANK_FILE = r"C:\Users\hp\OneDrive\Desktop\global-trade-supply-chain-intelligence\data\raw_data\world_bank_data\world_bank_country_year_2015_2024_20260707_222046.csv"
PROCESSED_OUTPUT_DIR = r"C:\Users\hp\OneDrive\Desktop\global-trade-supply-chain-intelligence\data\processed_data"

os.makedirs(PROCESSED_OUTPUT_DIR, exist_ok=True)

print("Raw World Bank file path:")
print(RAW_WORLD_BANK_FILE)
print("\nProcessed output folder:")
print(PROCESSED_OUTPUT_DIR)



# Loading the raw World Bank dataset
df_raw = pd.read_csv(RAW_WORLD_BANK_FILE)

print("Raw World Bank dataset loaded successfully.")
print(f"Rows: {df_raw.shape[0]:,}")
print(f"Columns: {df_raw.shape[1]:,}")

df_raw.head()



# Understanding the raw data structure

# Displaying the column names of the raw dataset
df_raw.columns.tolist()

# Checking info of the raw dataset
df_raw.info()

# Getting summary statistics of the raw dataset
df_raw.describe(include="all").T

# Checking for duplicate rows 
duplicate_rows = df_raw.duplicated().sum()
print(f"Exact duplicate rows in raw dataset: {duplicate_rows:,}")



# Checking for missing values in the raw dataset
missing_summary = pd.DataFrame({
    "missing_count": df_raw.isna().sum(),
    "missing_pct": (df_raw.isna().mean() * 100).round(2)
}).sort_values("missing_pct", ascending=False)

missing_summary



#### Checking the country-year structure
# Checking for unique values in key columns
print("Unique country codes:", df_raw["reporter_iso"].nunique(dropna=True))
print("Unique country names:", df_raw["reporter_name"].nunique(dropna=True))
print("Unique years:", sorted(df_raw["year"].dropna().unique().tolist()))



# Checking for duplicate country-year combinations
country_year_duplicates = df_raw.duplicated(subset=["reporter_iso", "year"]).sum()
print(f"Duplicate country-year rows: {country_year_duplicates:,}")


# Standardizing column names for consistency and clarity
column_rename_map = {
    "reporter_iso": "reporter_iso3",
    "reporter_name": "reporter_name",
    "year": "reference_year",
    "gdp_current_usd": "gdp_current_usd",
    "population_total": "population_total",
    "gdp_growth_annual_pct": "gdp_growth_annual_pct",
    "trade_pct_of_gdp": "trade_pct_of_gdp"
}

df = df_raw.rename(columns=column_rename_map).copy()

print("Column names standardized successfully.")
print(df.columns.tolist())



#### Keeping the columns needed for this project
columns_to_keep = [
    "reporter_iso3",
    "reporter_name",
    "reference_year",
    "gdp_current_usd",
    "population_total",
    "gdp_growth_annual_pct",
    "trade_pct_of_gdp"
]

df_clean = df[columns_to_keep].copy()

print("Created working cleaned World Bank dataframe.")
print(f"Rows: {df_clean.shape[0]:,}")
print(f"Columns kept: {df_clean.shape[1]}")
df_clean.head()



#### Cleaning string columns
df_clean["reporter_iso3"] = (
    df_clean["reporter_iso3"]
    .astype("string")
    .str.strip()
    .str.upper()
)

df_clean["reporter_name"] = (
    df_clean["reporter_name"]
    .astype("string")
    .str.strip()
)



#### Converting data types properly
df_clean["reference_year"] = pd.to_numeric(
    df_clean["reference_year"],
    errors="coerce"
).astype("Int64")

df_clean["population_total"] = pd.to_numeric(
    df_clean["population_total"],
    errors="coerce"
).astype("Int64")

numeric_float_cols = [
    "gdp_current_usd",
    "gdp_growth_annual_pct",
    "trade_pct_of_gdp"
]

for col in numeric_float_cols:
    df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")

df_clean.info()



#### Validate country ISO codes
invalid_iso_rows = df_clean[
    df_clean["reporter_iso3"].isna() |
    (df_clean["reporter_iso3"].str.len() != 3)
]

print(f"Rows with invalid ISO3 codes: {len(invalid_iso_rows):,}")

# Checking if there are any rows with invalid ISO3 codes
invalid_iso_rows.head()



#### Validate year coverage
print("Minimum reference year:", df_clean["reference_year"].min())
print("Maximum reference year:", df_clean["reference_year"].max())

print("\nReference year value counts:")
df_clean["reference_year"].value_counts().sort_index()



#### Reviewing missing values after cleaning
clean_missing_summary = pd.DataFrame({
    "missing_count": df_clean.isna().sum(),
    "missing_pct": (df_clean.isna().mean() * 100).round(2)
}).sort_values("missing_pct", ascending=False)

clean_missing_summary



# Checking for duplicate country-year combinations after cleaning
duplicate_country_year_rows = df_clean.duplicated(
    subset=["reporter_iso3", "reference_year"]
).sum()

print(f"Duplicate country-year rows after cleaning: {duplicate_country_year_rows:,}")



# Creating new columns to indicate the presence of data in key columns

df_clean["has_gdp_data"] = df_clean["gdp_current_usd"].notna().astype("Int64")
df_clean["has_population_data"] = df_clean["population_total"].notna().astype("Int64")
df_clean["has_gdp_growth_data"] = df_clean["gdp_growth_annual_pct"].notna().astype("Int64")
df_clean["has_trade_pct_gdp_data"] = df_clean["trade_pct_of_gdp"].notna().astype("Int64")

df_clean.head()



# Finalizing the cleaned dataset by reordering columns and sorting by country and year
final_column_order = [
    "reporter_iso3",
    "reporter_name",
    "reference_year",
    "gdp_current_usd",
    "population_total",
    "gdp_growth_annual_pct",
    "trade_pct_of_gdp",
    "has_gdp_data",
    "has_population_data",
    "has_gdp_growth_data",
    "has_trade_pct_gdp_data"
]

df_final = df_clean[final_column_order].copy()

df_final = df_final.sort_values(
    ["reporter_iso3", "reference_year"]
).reset_index(drop=True)

df_final.head()



#### Save the cleaned analytics-ready World Bank dataset
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

output_file_name = f"world_bank_country_year_clean_analytics_ready_{timestamp}.csv"
output_file_path = os.path.join(PROCESSED_OUTPUT_DIR, output_file_name)

df_final.to_csv(output_file_path, index=False)

print("Cleaned World Bank analytics-ready file saved successfully.")
print(output_file_path)



#### Final summary of the cleaned output
print("========== CLEANED WORLD BANK DATA SUMMARY ==========")
print(f"Rows: {df_final.shape[0]:,}")
print(f"Columns: {df_final.shape[1]:,}")
print(f"Country count: {df_final['reporter_iso3'].nunique():,}")
print(f"Reference year range: {df_final['reference_year'].min()} to {df_final['reference_year'].max()}")
print(f"Cleaned output file: {output_file_path}")