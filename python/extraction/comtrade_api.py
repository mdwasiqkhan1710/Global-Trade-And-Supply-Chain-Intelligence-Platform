
# Importing necessary libraries
import os
import time
import pandas as pd
import comtradeapicall
from datetime import datetime

from dotenv import load_dotenv
load_dotenv(override=True)  # Load environment variables from .env file


# ====================
# USER CONFIGURATION 
# ====================

SUBSCRIPTION_KEY = os.getenv("UN_COMTRADE_PRIMARY_KEY")      # UN Comtrade subscription key or API key
OUTPUT_DIRECTORY = os.getenv("OUTPUT_DIRECTORY")    # Folder where raw files will be stored

START_YEAR = 2015    # Starting year for data collection
END_YEAR = 2024      # Ending year for data collection

TYPE_CODE = "C"      # Commodity trade / goods trade
FREQ_CODE = "A"      # Annual data
CL_CODE = "HS"       # HS classification
CMD_CODE = "TOTAL"   # All goods total
FLOW_CODE = "X"      # Exports only

# Splitting the data into batches for processing to avoid timeouts and large payloads.
REPORTER_BATCH_SIZE = 25

# Delay b/w API calls to avoid hitting rate limits (in sec)
REQUEST_SLEEP_SECONDS = 1.5

# Whether to save every raw batch as its own CSV file
SAVE_RAW_BATCH_FILES = True

# Final combined output file format
FINAL_OUTPUT_FORMAT = "csv"



# ====================
# REPORTER CODE LIST
# ====================
# This list is the set of reporter country/area codes to query.

REPORTER_CODES = [
    "4", "8", "12", "20", "24", "28", "31", "32", "36", "40", "44", "48", "50", "51", "52", "56",
    "60", "64", "68", "70", "72", "76", "84", "90", "92", "96", "100", "104", "108", "112", "116",
    "120", "124", "132", "136", "140", "144", "148", "152", "156", "170", "174", "175", "178", "180",
    "184", "188", "191", "192", "196", "203", "204", "208", "212", "214", "218", "222", "226", "231",
    "232", "233", "234", "238", "242", "246", "251", "262", "266", "268", "270", "275", "288", "292",
    "296", "300", "304", "308", "312", "316", "320", "324", "328", "332", "336", "340", "344", "348",
    "352", "356", "360", "364", "368", "372", "376", "381", "388", "392", "398", "400", "404", "408",
    "410", "414", "417", "418", "422", "426", "428", "430", "434", "438", "440", "442", "446", "450",
    "454", "458", "462", "466", "470", "478", "480", "484", "492", "496", "498", "499", "500", "504",
    "508", "512", "516", "520", "524", "528", "531", "533", "540", "548", "554", "558", "562", "566",
    "570", "574", "578", "580", "583", "584", "585", "586", "591", "598", "600", "604", "608", "612",
    "616", "620", "624", "626", "634", "642", "643", "646", "652", "659", "660", "662", "666", "670",
    "674", "678", "682", "686", "688", "690", "694", "699", "702", "703", "704", "705", "706", "710",
    "716", "724", "728", "729", "740", "748", "752", "756", "760", "762", "764", "768", "772", "776",
    "780", "784", "788", "792", "795", "796", "798", "800", "804", "807", "818", "826", "834", "840",
    "842", "854", "858", "860", "862", "876", "882", "887", "894"
]



# Checking if correct API key and Output directory are loaded
# print(f"API Key: {SUBSCRIPTION_KEY}")
# print(f"Output Directory: {OUTPUT_DIRECTORY}")



# Helper Function to ensure output directory is available for storage
def ensure_directory(path: str) -> None:
    os.makedirs(path, exist_ok=True)

# Helper function to split a list into chunks of a specified size
def chunk_list(items, chunk_size):
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]

# Helper function to build a clean raw batch filename for one year + one reporter batch
def build_batch_file_name(year: int, batch_number: int) -> str:
    return f"comtrade_final_exports_total_{year}_batch_{batch_number:03d}.csv"



# =====================================================================
# STEP 1: Downlading one batch of data for one year + one reporter
# =====================================================================

def fetch_final_exports_batch(subscription_key, year, reporter_batch):
    reporter_str = ",".join(reporter_batch)

    df = comtradeapicall.getFinalData(
        subscription_key,
        typeCode=TYPE_CODE,
        freqCode=FREQ_CODE,
        clCode=CL_CODE,
        period=str(year),
        reporterCode=reporter_str,
        cmdCode=CMD_CODE,
        flowCode=FLOW_CODE,
        partnerCode=None,
        partner2Code=None,
        customsCode=None,
        motCode=None,
        maxRecords=100000,
        format_output="JSON",
        aggregateBy=None,
        breakdownMode="classic",
        countOnly=None,
        includeDesc=True
    )

    # If the API call returns None, return an empty DataFrame
    if df is None:
        return pd.DataFrame()

    # Convert the result to a DataFrame if it's not already one
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)

    return df



# ===================================================
# STEP 2: Downloading all years in reporter batches
# ===================================================

def download_world_bilateral_exports(
    subscription_key,
    output_dir,
    start_year,
    end_year,
    reporter_codes,
    reporter_batch_size=25,
    request_sleep_seconds=1.5,
    save_raw_batch_files=True
):
    
    ensure_directory(output_dir)

    all_frames = []
    raw_files = []

    for year in range(start_year, end_year + 1):
        print("\n" + "-" * 80)
        print(f"PROCESSING YEAR {year}")
        print("-" * 80)

        reporter_batches = list(chunk_list(reporter_codes, reporter_batch_size))

        for batch_idx, batch in enumerate(reporter_batches, start=1):
            print(f"\nYear {year} | Reporter batch {batch_idx}/{len(reporter_batches)}")
            print(f"Reporter codes in batch: {', '.join(batch)}")

            try:
                df_batch = fetch_final_exports_batch(
                    subscription_key=subscription_key,
                    year=year,
                    reporter_batch=batch
                )

                if df_batch.empty:
                    print(f"No rows returned for year {year}, batch {batch_idx}")
                    time.sleep(request_sleep_seconds)
                    continue

                # Add audit columns so you know how this data was pulled
                df_batch["download_year"] = year
                df_batch["reporter_batch_number"] = batch_idx
                df_batch["download_timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                print(f"Rows downloaded: {len(df_batch):,}")

                all_frames.append(df_batch)

                # Save raw batch CSV if enabled
                if save_raw_batch_files:
                    batch_file_name = build_batch_file_name(year, batch_idx)
                    batch_path = os.path.join(output_dir, batch_file_name)
                    df_batch.to_csv(batch_path, index=False)
                    raw_files.append(batch_path)
                    print(f"Saved raw batch file: {batch_path}")

            except Exception as e:
                print(f"ERROR in year {year}, batch {batch_idx}: {e}")

            # polite pause between calls
            time.sleep(request_sleep_seconds)

    # Combine everything into one DataFrame
    if all_frames:
        combined_df = pd.concat(all_frames, ignore_index=True)
    else:
        combined_df = pd.DataFrame()

    return raw_files, combined_df



# ============================================================
# STEP 3: Cleaning and saving the final combined output file
# ============================================================

def clean_combined_exports(df):
    if df.empty:
        return df

    cleaned = df.copy()

    # Drop exact duplicate rows if any
    cleaned = cleaned.drop_duplicates()

    # Standardize column names to lower_snake_case
    cleaned.columns = [
        col.strip().replace(" ", "_").replace("-", "_").lower()
        for col in cleaned.columns
    ]

    return cleaned



# ===============================================
# STEP 4: Saving the final combined output file
# ===============================================

def save_final_dataset(df: pd.DataFrame, output_dir: str, start_year: int, end_year: int, output_format="csv") -> str:
    ensure_directory(output_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = f"world_bilateral_exports_final_total_{start_year}_{end_year}_{timestamp}"

    if output_format.lower() == "parquet":
        output_path = os.path.join(output_dir, base_name + ".parquet")
        df.to_parquet(output_path, index=False)
    else:
        output_path = os.path.join(output_dir, base_name + ".csv")
        df.to_csv(output_path, index=False)

    return output_path



# =======================
# MAIN DRIVER FUNCTION
# =======================

def main():
    #Checking if the subscription key is set correctly
    if not SUBSCRIPTION_KEY or SUBSCRIPTION_KEY == "YOUR_COMTRADE_SUBSCRIPTION_KEY":
        raise ValueError(
            "Please replace SUBSCRIPTION_KEY with your actual UN Comtrade subscription key."
        )

    # Ensure the output directory exists
    ensure_directory(OUTPUT_DIRECTORY)

    print("-" * 80)
    print("UN COMTRADE FINAL WORLD BILATERAL EXPORTS DOWNLOAD PIPELINE")
    print("-" * 80)

    raw_files, combined_df = download_world_bilateral_exports(
        subscription_key=SUBSCRIPTION_KEY,
        output_dir=OUTPUT_DIRECTORY,
        start_year=START_YEAR,
        end_year=END_YEAR,
        reporter_codes=REPORTER_CODES,
        reporter_batch_size=REPORTER_BATCH_SIZE,
        request_sleep_seconds=REQUEST_SLEEP_SECONDS,
        save_raw_batch_files=SAVE_RAW_BATCH_FILES
    )

    print("\nDownload phase completed.")
    print(f"Raw batch files saved: {len(raw_files)}")
    print(f"Combined rows before cleaning: {len(combined_df):,}")

    combined_df = clean_combined_exports(combined_df)

    print(f"Combined rows after cleaning : {len(combined_df):,}")

    if combined_df.empty:
        print("No data was downloaded. Please review your API key, parameters, and rate limits.")
        return

    final_file = save_final_dataset(
        df=combined_df,
        output_dir=OUTPUT_DIRECTORY,
        start_year=START_YEAR,
        end_year=END_YEAR,
        output_format=FINAL_OUTPUT_FORMAT
    )

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()