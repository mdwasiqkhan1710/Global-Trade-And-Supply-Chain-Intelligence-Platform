# Importing necessary libraries
import os
import time
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv(override=True)  # Load environment variables from .env file



# ====================
# User Configuration 
# ====================
OUTPUT_DIR = os.getenv("OUTPUT_DIRECTORY_WORLD_BANK")

START_YEAR = 2015                   # Starting year for data collection
END_YEAR = 2024                     # Ending year for data collection
FINAL_OUTPUT_FORMAT = "csv"         # Final output format for the data
SAVE_RAW_INDICATOR_FILES = True     # Flag to save raw indicator files
MAX_RETRIES = 3                     # Maximum number of retries for failed requests
RETRY_BACKOFF_SECONDS = 2           # Backoff time between retries
REQUEST_SLEEP_SECONDS = 1.0         # Sleep time between requests



# Check if OUTPUT_DIR is available
if not OUTPUT_DIR:
    raise ValueError("OUTPUT_DIRECTORY_WORLD_BANK was not found in your .env file. Please add it and try again.")


# Defining the indicators to fetch from the World Bank API
INDICATORS = {
    "NY.GDP.MKTP.CD": "gdp_current_usd",
    "SP.POP.TOTL": "population_total",
    "NY.GDP.MKTP.KD.ZG": "gdp_growth_annual_pct",
    "NE.TRD.GNFS.ZS": "trade_pct_of_gdp"
}
INDICATORS



# ====================
# Helper Functions
# ====================
# Ensure the output directory exists
def ensure_directory(path: str) -> None:
    os.makedirs(path, exist_ok=True)



# Function to build the World Bank API URL
def build_world_bank_url(indicator_code: str, start_year: int, end_year: int) -> str:
    return (
        f"https://api.worldbank.org/v2/country/all/indicator/{indicator_code}"
        f"?format=json&date={start_year}:{end_year}&per_page=20000"
    )



# Function to fetch JSON data from the World Bank API with retries
def fetch_json_with_retries(url: str, max_retries: int = 3, backoff_seconds: int = 2):
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, timeout=120)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt == max_retries:
                raise Exception(
                    f"World Bank API request failed after {max_retries} attempts.\n"
                    f"URL: {url}\nError: {e}"
                )
            wait_time = backoff_seconds ** attempt
            print(f"Request failed (attempt {attempt}/{max_retries})")
            print(f"Retrying in {wait_time} seconds...")
            time.sleep(wait_time)



# Function to filter out aggregate region codes from the DataFrame
AGGREGATE_REGION_CODES = {
    "AFE", "AFW", "ARB", "CEB", "CSS", "EAP", "EAR", "EAS", "ECA", "ECS",
    "EMU", "EUU", "FCS", "HIC", "HPC", "IBD", "IBT", "IDA", "IDB", "IDX",
    "INX", "LAC", "LCN", "LDC", "LIC", "LMC", "LMY", "LTE", "MEA", "MIC",
    "MNA", "NAC", "OED", "OSS", "PRE", "PSS", "PST", "SAS", "SSA", "SSF",
    "SST", "TEA", "TEC", "TLA", "TMN", "TSA", "TSS", "UMC", "WLD"
}

def filter_country_rows(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    filtered = df.copy()
    filtered = filtered[filtered["reporter_iso"].notna()]
    filtered = filtered[filtered["reporter_iso"] != ""]
    filtered = filtered[filtered["reporter_iso"].str.len() == 3]
    filtered = filtered[~filtered["reporter_iso"].isin(AGGREGATE_REGION_CODES)]
    return filtered



# Function to fetch World Bank indicator data and return it as a DataFrame
def fetch_world_bank_indicator(indicator_code: str, indicator_name: str, start_year: int, end_year: int) -> pd.DataFrame:
    url = build_world_bank_url(indicator_code, start_year, end_year)

    print(f"\nDownloading indicator: {indicator_code} -> {indicator_name}")
    print(f"URL: {url}")

    data = fetch_json_with_retries(
        url=url,
        max_retries=MAX_RETRIES,
        backoff_seconds=RETRY_BACKOFF_SECONDS
    )

    if not isinstance(data, list) or len(data) < 2 or data[1] is None:
        print(f"No usable data returned for indicator {indicator_code}")
        return pd.DataFrame(columns=["reporter_name", "reporter_iso", "year", indicator_name])

    records = data[1]
    rows = []

    for record in records:
        country = record.get("country", {})
        rows.append({
            "reporter_name": country.get("value"),
            "reporter_iso": record.get("countryiso3code"),
            "year": pd.to_numeric(record.get("date"), errors="coerce"),
            indicator_name: record.get("value")
        })

    df = pd.DataFrame(rows)

    if df.empty:
        return df

    df = df[df["year"].notna()]
    df["year"] = df["year"].astype(int)
    df = df[(df["year"] >= start_year) & (df["year"] <= end_year)]
    df[indicator_name] = pd.to_numeric(df[indicator_name], errors="coerce")
    df = filter_country_rows(df)
    df = df[["reporter_name", "reporter_iso", "year", indicator_name]].drop_duplicates()

    return df



# Function to save the raw indicator DataFrame to a CSV file
def save_raw_indicator_file(df: pd.DataFrame, output_dir: str, indicator_code: str, indicator_name: str) -> str:
    ensure_directory(output_dir)
    file_name = f"wb_{indicator_name}_{indicator_code}.csv"
    output_path = os.path.join(output_dir, file_name)
    df.to_csv(output_path, index=False)
    return output_path



# Function to download multiple World Bank indicators and save them to files
def download_world_bank_indicators(
    indicators: dict,
    output_dir: str,
    start_year: int,
    end_year: int,
    save_raw_indicator_files: bool = True,
    request_sleep_seconds: float = 1.0
):
    indicator_frames = {}

    for indicator_code, indicator_name in indicators.items():
        try:
            df = fetch_world_bank_indicator(
                indicator_code=indicator_code,
                indicator_name=indicator_name,
                start_year=start_year,
                end_year=end_year
            )

            print(f"Rows downloaded for {indicator_name}: {len(df):,}")
            indicator_frames[indicator_name] = df

            if save_raw_indicator_files:
                raw_path = save_raw_indicator_file(
                    df=df,
                    output_dir=output_dir,
                    indicator_code=indicator_code.replace(".", "_"),
                    indicator_name=indicator_name
                )
                print(f"Saved raw indicator file: {raw_path}")

        except Exception as e:
            print(f"ERROR while downloading {indicator_code} ({indicator_name}): {e}")
            indicator_frames[indicator_name] = pd.DataFrame(
                columns=["reporter_name", "reporter_iso", "year", indicator_name]
            )

        time.sleep(request_sleep_seconds)

    return indicator_frames



# Function to combine multiple World Bank indicator DataFrames into a single DataFrame
def combine_world_bank_indicators(indicator_frames: dict) -> pd.DataFrame:
    if not indicator_frames:
        return pd.DataFrame()

    merged_df = None

    for _, df in indicator_frames.items():
        if df.empty:
            continue
        if merged_df is None:
            merged_df = df.copy()
        else:
            merged_df = merged_df.merge(
                df,
                on=["reporter_name", "reporter_iso", "year"],
                how="outer"
            )

    if merged_df is None:
        return pd.DataFrame()

    return merged_df



# Function to clean and standardize the combined World Bank DataFrame
def clean_world_bank_dataset(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    cleaned = df.copy().drop_duplicates()
    cleaned["reporter_name"] = cleaned["reporter_name"].astype(str).str.strip()
    cleaned["reporter_iso"] = cleaned["reporter_iso"].astype(str).str.strip().str.upper()
    cleaned = cleaned.sort_values(["reporter_iso", "year"]).reset_index(drop=True)

    preferred_order = [
        "reporter_iso",
        "reporter_name",
        "year",
        "gdp_current_usd",
        "population_total",
        "gdp_growth_annual_pct",
        "trade_pct_of_gdp"
    ]

    existing_columns = [col for col in preferred_order if col in cleaned.columns]
    remaining_columns = [col for col in cleaned.columns if col not in existing_columns]
    return cleaned[existing_columns + remaining_columns]



# Function to save the final cleaned World Bank DataFrame to a file
def save_final_world_bank_dataset(
    df: pd.DataFrame,
    output_dir: str,
    start_year: int,
    end_year: int,
    output_format: str = "csv"
) -> str:
    ensure_directory(output_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = f"world_bank_country_year_{start_year}_{end_year}_{timestamp}"

    if output_format.lower() == "parquet":
        output_path = os.path.join(output_dir, base_name + ".parquet")
        df.to_parquet(output_path, index=False)
    else:
        output_path = os.path.join(output_dir, base_name + ".csv")
        df.to_csv(output_path, index=False)

    return output_path



# Main function to run the World Bank data extraction pipeline
def run_world_bank_pipeline():
    ensure_directory(OUTPUT_DIR)

    print("=" * 90)
    print("WORLD BANK DATA EXTRACTION PIPELINE")
    print("=" * 90)
    print(f"Output directory         : {OUTPUT_DIR}")
    print(f"Years                    : {START_YEAR} to {END_YEAR}")
    print("Indicators to download:")
    for code, name in INDICATORS.items():
        print(f"  - {code} -> {name}")
    print(f"Save raw indicator files : {SAVE_RAW_INDICATOR_FILES}")
    print(f"Final output format      : {FINAL_OUTPUT_FORMAT}")
    print("=" * 90)

    indicator_frames = download_world_bank_indicators(
        indicators=INDICATORS,
        output_dir=OUTPUT_DIR,
        start_year=START_YEAR,
        end_year=END_YEAR,
        save_raw_indicator_files=SAVE_RAW_INDICATOR_FILES,
        request_sleep_seconds=REQUEST_SLEEP_SECONDS
    )

    combined_df = combine_world_bank_indicators(indicator_frames)
    print(f"\nRows before final cleaning: {len(combined_df):,}")

    combined_df = clean_world_bank_dataset(combined_df)
    print(f"Rows after final cleaning : {len(combined_df):,}")

    if combined_df.empty:
        print("No World Bank data was downloaded.")
        return None, None

    final_file = save_final_world_bank_dataset(
        df=combined_df,
        output_dir=OUTPUT_DIR,
        start_year=START_YEAR,
        end_year=END_YEAR,
        output_format=FINAL_OUTPUT_FORMAT
    )

    print("\nPipeline completed successfully.")
    print(f"Final World Bank dataset saved at:\n{final_file}")

    return combined_df, final_file



# Entry point for the script
if __name__ == "__main__":
    combined_df, final_file = run_world_bank_pipeline()



# Display the first few rows of the combined DataFrame and the final file path
if combined_df is not None:
    print(combined_df.head())
    print("\nFinal file path:")
    print(final_file)