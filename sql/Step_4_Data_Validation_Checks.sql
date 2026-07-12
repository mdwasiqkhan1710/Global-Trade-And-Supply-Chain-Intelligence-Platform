-- Data Validation : Checking if all the data has been uploaded successfully.alter

-- Ensuring that we are using correct database:
USE global_trade_analytics_db;

SHOW TABLES;


-- Starting Validation Checks in US Comtrade Dataset:- 

-- Checking total rows:
SELECT 
	COUNT(comtrade_fact_id) AS total_rows 
FROM 
	fact_comtrade_exports_dataset;
    
-- Checking for NULL values in Non-Null columns:
SELECT
	SUM(reference_year IS NULL) 				AS reference_year_nulls,
    SUM(period IS NULL) 						AS period_nulls,
    SUM(reporter_code IS NULL) 					AS reporter_code_nulls,
    SUM(reporter_iso3 IS NULL) 					AS reporter_iso3_nulls,
    SUM(reporter_name IS NULL) 					AS reporter_name_nulls,
    SUM(partner_code IS NULL) 					AS partner_code_nulls,
    SUM(partner_iso3 IS NULL) 					AS partner_iso3_nulls,
    SUM(partner_name IS NULL) 					AS partner_name_nulls,
    SUM(is_world_partner IS NULL) 				AS is_world_partner_nulls,
    SUM(trade_value_usd IS NULL) 				AS trade_value_usd_nulls,
    SUM(flow_code IS NULL) 						AS flow_code_nulls,
    SUM(flow_name IS NULL) 						AS flow_name_nulls,
    SUM(commodity_code IS NULL) 				AS commodity_code_nulls,
    SUM(commodity_description IS NULL) 			AS commodity_description_nulls,
    SUM(type_code IS NULL) 						AS type_code_nulls,
    SUM(freq_code IS NULL) 						AS freq_code_nulls,
    SUM(classification_revision_code IS NULL) 	AS classification_revision_code_nulls,
    SUM(is_reported IS NULL) 					AS is_reported_nulls,
    SUM(is_aggregate IS NULL) 					AS is_aggregate_nulls
FROM 
	fact_comtrade_exports_dataset;

-- Checking for Nullable FOB values:
SELECT
    COUNT(*) AS total_rows,
    COUNT(fob_value_usd) AS non_null_fob_values,
    SUM(fob_value_usd IS NULL) AS null_fob_values
FROM 
	fact_comtrade_exports_dataset;

-- Checking Boolean Columns: 
SELECT DISTINCT is_world_partner
FROM fact_comtrade_exports_dataset;

SELECT DISTINCT is_reported
FROM fact_comtrade_exports_dataset;

SELECT DISTINCT is_aggregate
FROM fact_comtrade_exports_dataset;

-- Verifying Date range:
SELECT
    MIN(reference_year) AS minimum_year,
    MAX(reference_year) AS maximum_year
FROM fact_comtrade_exports_dataset;

-- Checking download_timestamp values:
SELECT
    MIN(download_timestamp) AS first_download_timestamp,
    MAX(download_timestamp) AS last_download_timestamp
FROM fact_comtrade_exports_dataset;

-- Verifying diff countries: 
SELECT
    COUNT(DISTINCT reporter_iso3) AS total_reporting_countries,
    COUNT(DISTINCT partner_iso3) AS total_partner_countries
FROM fact_comtrade_exports_dataset;

-- Validation Checks for World Bank dataset:-

-- Checking total_rows:
SELECT 
	COUNT(wb_fact_id) AS total_rows 
FROM 
	fact_world_bank_dataset;
    
-- Checking for NULL values in Non-Null columns:
SELECT
	SUM(reporter_iso3 IS NULL) 					AS reporter_iso3_nulls,
    SUM(reporter_name IS NULL) 					AS reporter_name_nulls,
    SUM(reference_year IS NULL) 				AS reference_year_nulls,
    SUM(has_gdp_data IS NULL) 					AS has_gdp_data_nulls,
    SUM(has_population_data IS NULL) 			AS has_population_data_nulls,
    SUM(has_gdp_growth_data IS NULL) 			AS has_gdp_growth_data_nulls,
    SUM(has_trade_pct_gdp_data IS NULL) 		AS has_trade_pct_gdp_data_nulls
FROM fact_world_bank_dataset;

-- Checking starting and ending year available
SELECT
	MIN(reference_year) AS min_year,
    MAX(reference_year) AS max_year
FROM
	fact_world_bank_dataset;

-- Checking Boolean values:
SELECT
	DISTINCT(has_gdp_data)
FROM 
	fact_world_bank_dataset;

SELECT
	DISTINCT(has_population_data)
FROM 
	fact_world_bank_dataset;

SELECT
	DISTINCT(has_gdp_growth_data)
FROM 
	fact_world_bank_dataset;

SELECT
	DISTINCT(has_trade_pct_gdp_data)
FROM 
	fact_world_bank_dataset;
    
SELECT * FROM fact_world_bank_dataset;