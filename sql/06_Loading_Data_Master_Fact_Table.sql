-- Populating Master Fact Table by Joining Data from Comtrade and World Bank both.

INSERT INTO fact_global_trade_intelligence_dataset
(
    reporter_iso3,
    reporter_name,
    partner_iso3,
    partner_name,
    reference_year,
    trade_value_usd,
    fob_value_usd,
    commodity_code,
    commodity_description,
    classification_revision_code,
    gdp_current_usd,
    population_total,
    gdp_growth_annual_pct,
    trade_pct_of_gdp,
    has_gdp_data,
    has_population_data,
    has_gdp_growth_data,
    has_trade_pct_gdp_data
)
SELECT 
	ct.reporter_iso3,
    ct.reporter_name,
    ct.partner_iso3,
    ct.partner_name,
    ct.reference_year,
    ct.trade_value_usd,
    ct.fob_value_usd,
    ct.commodity_code,
    ct.commodity_description,
    ct.classification_revision_code,
    wb.gdp_current_usd,
    wb.population_total,
    wb.gdp_growth_annual_pct,
    wb.trade_pct_of_gdp,
    wb.has_gdp_data,
    wb.has_population_data,
    wb.has_gdp_growth_data,
    wb.has_trade_pct_gdp_data
FROM 
	fact_comtrade_exports_dataset ct
LEFT JOIN
    fact_world_bank_dataset wb
ON
	ct.reporter_iso3 = wb.reporter_iso3
AND
    ct.reference_year = wb.reference_year;


-- Creating Indexes on Master Fact Table:

CREATE INDEX idx_master_reporter_year ON fact_global_trade_intelligence_dataset(reporter_iso3, reference_year);
CREATE INDEX idx_master_partner_year ON fact_global_trade_intelligence_dataset(partner_iso3, reference_year);
CREATE INDEX idx_master_reporter_partner_year ON fact_global_trade_intelligence_dataset(reporter_iso3, partner_iso3, reference_year);
CREATE INDEX idx_master_commodity ON fact_global_trade_intelligence_dataset(commodity_code);
CREATE INDEX idx_master_year ON fact_global_trade_intelligence_dataset(reference_year);

SHOW INDEXES FROM fact_global_trade_intelligence_dataset;

-- Updating Statistics:
ANALYZE TABLE fact_global_trade_intelligence_dataset;


-- Validating the Uploaded Data in fact_global_trade_intelligence_dataset Table.

-- 1) Checking sample data:
SELECT 
	*
FROM
	fact_global_trade_intelligence_dataset
LIMIT 
	10;

-- 2) Cheking total records:
SELECT 
	COUNT(*) AS total_records
FROM
	fact_global_trade_intelligence_dataset;

-- 3) Checking missing world Bank values:
SELECT
	 COUNT(*) AS missing_gdp_values
FROM 
	fact_global_trade_intelligence_dataset
WHERE 
	gdp_current_usd IS NULL;

-- 4) Checking India as example:
SELECT 
	*
FROM 
	fact_global_trade_intelligence_dataset
WHERE 
	reporter_iso3 = 'IND' AND 
    reference_year = 2024;