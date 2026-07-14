-- 1) Creating the database
CREATE DATABASE IF NOT EXISTS global_trade_analytics_db;

-- 2) Using the Database
USE global_trade_analytics_db;

-- 3) Dropping both tables first if they already exists
DROP TABLES IF EXISTS fact_comtrade_exports_dataset CASCADE;
DROP TABLES IF EXISTS fact_world_bank_dataset CASCADE;

-- 4) Creating the Tables to store US Comtrade & World Bank Data
CREATE TABLE fact_world_bank_dataset(
	wb_fact_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT, -- Creating automatic id for each row in table
    reporter_iso3 VARCHAR(10) NOT NULL,
    reporter_name VARCHAR(150) NOT NULL,
    reference_year SMALLINT NOT NULL,
    gdp_current_usd DOUBLE NULL,
    population_total BIGINT NULL,
    gdp_growth_anual_pct DOUBLE NULL,
    trade_pct_of_gdp DOUBLE NULL,
    has_gdp_data BOOLEAN NOT NULL,
    has_population_data BOOLEAN NOT NULL,
    has_gdp_growth_data BOOLEAN NOT NULL,
    has_trade_pct_data BOOLEAN NOT NULL,
    
    CONSTRAINT pk_fact_world_bank_country_year PRIMARY KEY (wb_fact_id),
    
    -- This will ensure that there is only one record per reporter country per year.
    CONSTRAINT uq_world_bank_reporter_year UNIQUE (reporter_iso3, reference_year)
);


CREATE TABLE fact_comtrade_exports_dataset(
	comtrade_fact_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,  -- Creating automatic id for each row in table
    reference_year SMALLINT NOT NULL,
    period SMALLINT NOT NULL,
    reporter_code INT NOT NULL,
    reporter_iso3 VARCHAR(10) NOT NULL,
    reporter_name VARCHAR(150) NOT NULL,
    partner_code INT NOT NULL,
    partner_iso3 VARCHAR(10) NOT NULL,
    partner_name VARCHAR(150) NOT NULL,
    is_world_partner BOOLEAN NOT NULL,
    trade_value_usd DOUBLE NOT NULL,
    fob_value_usd DOUBLE NULL,
    flow_code VARCHAR(10) NOT NULL,
    flow_name VARCHAR(100) NOT NULL,
    commodity_code VARCHAR(50) NOT NULL,
    commodity_description VARCHAR(255) NOT NULL,
    type_code VARCHAR(10) NOT NULL,
    freq_code VARCHAR(10) NOT NULL,
    classification_revision_code VARCHAR(20) NOT NULL,
    is_reported BOOLEAN NOT NULL,
    is_aggregate BOOLEAN NOT NULL,
    download_timestamp DATETIME NOT NULL,
    
    CONSTRAINT pk_fact_comtrade_exports_dataset PRIMARY KEY (comtrade_fact_id),
    
    -- This will ensure that there is only one record per combination of below 6 columns
    CONSTRAINT uq_comtrade_business_grain UNIQUE (reference_year, reporter_code, partner_code, flow_code, commodity_code, classification_revision_code)
);


-- Establishing relationships between Tables/Databases (Using Foreign Keys)
ALTER TABLE fact_comtrade_exports_dataset
ADD CONSTRAINT fk_relationship_comtrade_dataset_to_world_bank_dataset
			FOREIGN KEY (reporter_iso3, reference_year) 
            REFERENCES fact_world_bank_dataset (reporter_iso3, reference_year) 
            ON UPDATE CASCADE 
            ON DELETE RESTRICT;