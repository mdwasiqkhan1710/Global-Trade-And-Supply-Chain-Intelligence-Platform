-- Creating Master Fact File, i.e. Combining both Comtrade and World Bank datasets to create final dataset.
-- Source Tables : fact_comtrade_exports_dataset and fact_world_bank_dataset.

-- Ensuring that I am using correct DB:
USE global_trade_analytics_db;

-- Removing any master table if it exists:
DROP TABLE IF EXISTS fact_global_trade_intelligence_dataset;

-- Creating new table:
CREATE TABLE fact_global_trade_intelligence_dataset
(
	trade_economic_id 				BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY, -- Creating auto incrementing id for each row in table.
    reporter_iso3 					VARCHAR(10) NOT NULL,
    reporter_name 					VARCHAR(150) NOT NULL,
    partner_iso3 					VARCHAR(10),
    partner_name 					VARCHAR(150),
    reference_year 					SMALLINT NOT NULL,
    trade_value_usd 				DOUBLE,
    fob_value_usd 					DOUBLE,
    commodity_code 					VARCHAR(50),
    commodity_description 			VARCHAR(255),
    classification_code 			VARCHAR(50),
    classification_revision_code 	VARCHAR(50),
    gdp_current_usd 				DOUBLE,
    population_total 				BIGINT,
    gdp_growth_annual_pct 			DOUBLE,
    trade_pct_of_gdp 				DOUBLE,
    has_gdp_data 					BOOLEAN,
    has_population_data 			BOOLEAN,
    has_gdp_growth_data 			BOOLEAN,
    has_trade_pct_gdp_data 			BOOLEAN,
    created_at 						TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);