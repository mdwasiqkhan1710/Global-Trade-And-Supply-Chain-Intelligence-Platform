-- Creating Views for analysis as per requirement

-- Ensuring that I am using correct DB:
USE global_trade_analytics_db;

-- Dropping already existing views (if any):
DROP VIEW IF EXISTS vw_country_yearly_exports;
DROP VIEW IF EXISTS vw_partner_trade_analysis;
DROP VIEW IF EXISTS vw_top_exporting_countries;
DROP VIEW IF EXISTS vw_commodity_exports;
DROP VIEW IF EXISTS vw_trade_economic_profile;
DROP VIEW IF EXISTS vw_trade_growth_indicators;
DROP VIEW IF EXISTS vw_country_trade_summary;
DROP VIEW IF EXISTS vw_dashboard_dataset;


-- Creating First View : vw_country_yearly_exports
-- This will provide yearly exports performance of every reporting country:
CREATE VIEW 
	vw_country_yearly_exports
AS 
SELECT 
	reporter_iso3, 
    reporter_name, 
    reference_year, 
    SUM(trade_value_usd) 				AS total_exports_usd, 
    SUM(fob_value_usd) 					AS total_fob_exports_usd,
    COUNT(*) 							AS total_trade_transactions,
    COUNT(DISTINCT partner_iso3) 		AS unique_trade_partners,
    COUNT(DISTINCT commodity_code) 		AS unique_exported_commodities,
    ROUND(AVG(trade_value_usd),2) 		AS avg_trade_value,
    MAX(trade_value_usd) 				AS highest_single_trade,
    MIN(trade_value_usd) 				AS lowest_single_trade
FROM 
	fact_global_trade_intelligence_dataset
GROUP BY
	reporter_iso3,
    reporter_name,
    reference_year;


-- Creating view : vw_partner_trade_analysis
-- This will provide bilateral trade analysis between reporting country and partner country:
CREATE VIEW 
	vw_partner_trade_analysis
AS
SELECT 
	reporter_iso3,
    reporter_name,
    partner_iso3,
    partner_name,
    reference_year,
    SUM(trade_value_usd) 					AS total_trade_value,
    SUM(fob_value_usd) 						AS total_fob_value,
    COUNT(*) 								AS total_shipments,
    COUNT(DISTINCT commodity_code) 			AS commodities_exported,
    ROUND(AVG(trade_value_usd), 2) 			AS avg_trade_value,
    MAX(trade_value_usd) 					AS largest_trade_transaction
FROM
	fact_global_trade_intelligence_dataset
GROUP BY
	reporter_iso3,
    reporter_name,
    partner_iso3,
    partner_name,
    reference_year;


-- Creating view : vw_top_exporting_countries
-- This will provide yearly export performance aggregated at the reporting country level:
CREATE VIEW 
	vw_top_exporting_countries
AS
SELECT 
	reference_year,
    reporter_iso3,
    reporter_name,
    SUM(trade_value_usd)                    AS total_exports_usd,
    SUM(fob_value_usd)                      AS total_fob_exports_usd,
    COUNT(DISTINCT partner_iso3)            AS total_export_markets,
    COUNT(DISTINCT commodity_code)          AS total_exported_commodities,
    ROUND(AVG(trade_value_usd),2)           AS average_transaction_value,
    MAX(trade_value_usd)                    AS largest_export_transaction,
    MIN(trade_value_usd)                    AS smallest_export_transaction
FROM
	fact_global_trade_intelligence_dataset
GROUP BY
	reference_year,
	reporter_iso3,
    reporter_name;


-- Creating view : vw_commodity_exports
-- This will provide export performance for every commodity by reporting country and reporting year:
CREATE VIEW 
	vw_commodity_exports
AS 
SELECT
	reference_year,
    reporter_iso3,
    reporter_name,
    commodity_code,
    commodity_description,
    SUM(trade_value_usd)                   AS total_exports_usd,
    SUM(fob_value_usd)                     AS total_fob_exports_usd,
    COUNT(*)                               AS total_trade_transactions,
    COUNT(DISTINCT partner_iso3)           AS total_export_destinations,
    ROUND(AVG(trade_value_usd),2)          AS average_trade_value,
    MAX(trade_value_usd)                   AS largest_trade_value,
    MIN(trade_value_usd)                   AS smallest_trade_value
FROM
fact_global_trade_intelligence_dataset
GROUP BY
	reference_year,
    reporter_iso3,
    reporter_name,
    commodity_code,
    commodity_description;


-- Creating view: vw_trade_economic_profile
-- This will provide consolidated economic profile of each reporting country by combining trade performance with macroeconomic indicators.
CREATE VIEW
	vw_trade_economic_profile
AS
SELECT
	reporter_iso3,
    reporter_name,
    reference_year,
    SUM(trade_value_usd) 														AS total_exports_usd,
    MAX(gdp_current_usd) 														AS gdp_current_usd,
    MAX(population_total) 														AS population_total,
    MAX(gdp_growth_annual_pct) 													AS gdp_growth_annual_pct,
    MAX(trade_pct_of_gdp) 														AS trade_pct_of_gdp,
    ROUND( SUM(trade_value_usd) / NULLIF(MAX(population_total), 0), 2) 			AS exports_per_capita, -- Calculating exports per capita income of country
    ROUND((SUM(trade_value_usd) / NULLIF(MAX(gdp_current_usd), 0)) * 100, 2) 	AS exports_pct_of_gdp -- Export % of GDP Ratio calculation
FROM
	fact_global_trade_intelligence_dataset
GROUP BY
	reporter_iso3,
    reporter_name,
    reference_year;


-- Creating view: vw_trade_growth_indicators
-- This will provide Year-over-Year export growth of countries. Note: Here, I am using SQL Window Functions:
CREATE VIEW
	vw_trade_growth_indicators
AS
SELECT
	reporter_iso3,
    reporter_name,
    reference_year,
    total_exports_usd,
    previous_year_exports,
    ROUND(((total_exports_usd - previous_year_exports) / NULLIF(previous_year_exports,0)) * 100, 2) AS yoy_export_growth_pct
FROM
	(
	SELECT
		reporter_iso3,
		reporter_name,
		reference_year,
		SUM(trade_value_usd) AS total_exports_usd,
		LAG(SUM(trade_value_usd)) OVER 
        (PARTITION BY reporter_iso3 ORDER BY reference_year)AS previous_year_exports
	FROM
		fact_global_trade_intelligence_dataset
	GROUP BY
		reporter_iso3,
        reporter_name,
        reference_year
	) yearly_trade;