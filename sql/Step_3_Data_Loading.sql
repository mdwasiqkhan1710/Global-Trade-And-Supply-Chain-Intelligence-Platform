-- Inserting Data from processed datasets into the Database.
-- Note : Processed Datasets are extracted, cleaned & transformed using Python and finally saved in Global-Trade-And-Supply-Chain-Intelligence-Platform/data > processed_data.


-- Ensuring that we are using correct Database to avoid errors.
USE global_trade_analytics_db;


-- Temporarily disabiling the foreign key check
SET FOREIGN_KEY_CHECKS = 0;


-- Receiving error -: Unknown column 'gdp_growth_annual_pct' and 'has_trade_pct_data' in 'field list' while inserting data because I provided incorrect column name
-- Thus updating the correct column name in database
ALTER TABLE fact_world_bank_dataset
RENAME COLUMN gdp_growth_anual_pct TO gdp_growth_annual_pct;

ALTER TABLE fact_world_bank_dataset
RENAME COLUMN has_trade_pct_data TO has_trade_pct_gdp_data;


-- Loading the world_bank data
LOAD DATA INFILE
	"C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/world_bank_country_year_clean_analytics_ready_20260709_021503.csv"
INTO TABLE 
	fact_world_bank_dataset
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(reporter_iso3, 
reporter_name, 
reference_year, 
@gdp_current_usd, 
population_total, 
@gdp_growth_annual_pct, 
@trade_pct_of_gdp, 
@has_gdp_data, 
@has_population_data, 
@has_gdp_growth_data, 
@has_trade_pct_gdp_data)
SET
	gdp_current_usd =
	NULLIF(@gdp_current_usd,''), -- Setting gdp_current_usd NULL if empty column is found in csv file

	gdp_growth_annual_pct =
	NULLIF(@gdp_growth_annual_pct,''), -- Setting gdp_growth_annual_pct NULL if empty column is found in csv file

	trade_pct_of_gdp =
	NULLIF(@trade_pct_of_gdp,''), -- Setting trade_pct_of_gdp NULL if empty column is found in csv file

	has_gdp_data =
    CASE 
		WHEN LOWER(TRIM(@has_gdp_data)) = 'true' THEN 1
        WHEN LOWER(TRIM(@has_gdp_data)) = 'false' THEN 0
        ELSE 0
	END,
    
    has_population_data =
    CASE 
		WHEN LOWER(TRIM(@has_population_data)) = 'true' THEN 1
        WHEN LOWER(TRIM(@has_population_data)) = 'false' THEN 0
        ELSE 0
	END,
    
    has_gdp_growth_data =
    CASE 
		WHEN LOWER(TRIM(@has_gdp_growth_data)) = 'true' THEN 1
        WHEN LOWER(TRIM(@has_gdp_growth_data)) = 'false' THEN 0
        ELSE 0
	END,
    
    has_trade_pct_gdp_data =
    CASE 
		WHEN LOWER(TRIM(@has_trade_pct_gdp_data)) = 'true' THEN 1
        WHEN LOWER(TRIM(@has_trade_pct_gdp_data)) = 'false' THEN 0
        ELSE 0
	END;

-- Loading the US ComTrade Data
LOAD DATA INFILE
	"C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/comtrade_exports_clean_analytics_ready_20260709_020129.csv"
INTO TABLE 
	fact_comtrade_exports_dataset
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
reference_year,
period,
reporter_code,
reporter_iso3,
reporter_name,
partner_code,
partner_iso3,
partner_name,
@is_world_partner,
trade_value_usd,
@fob_value_usd,
flow_code,
flow_name,
commodity_code,
commodity_description,
type_code,
freq_code,
classification_revision_code,
@is_reported,
@is_aggregate,
download_timestamp
)
SET
	fob_value_usd =
	CASE
		WHEN @fob_value_usd = ''
			OR UPPER(@fob_value_usd) = 'NAN'
		THEN NULL
		ELSE @fob_value_usd
	END,
	is_world_partner =
	CASE
		WHEN @is_world_partner='True' THEN 1
		WHEN @is_world_partner='False' THEN 0
		ELSE NULL
	END,

	is_reported =
	CASE
		WHEN @is_reported='True' THEN 1
		WHEN @is_reported='False' THEN 0
		ELSE NULL
	END,

	is_aggregate =
	CASE
		WHEN @is_aggregate='True' THEN 1
		WHEN @is_aggregate='False' THEN 0
		ELSE NULL
	END
;


-- Enabiling Foreign Key checks again
SET FOREIGN_KEY_CHECKS = 1;