-- Created Dashboard Ready Views.

-- Creating view: vw_country_trade_summary
-- This will provide a comprehensive yearly trade summary for each reporting country, including export performance, macroeconomic indicators, and global rankings.
CREATE VIEW 
	vw_country_trade_summary 
AS
WITH 
	country_summary 
    AS
    (
		SELECT
			reporter_iso3,
            reporter_name,
            reference_year,
            SUM(trade_value_usd) AS total_exports_usd,
			SUM(fob_value_usd) AS total_fob_exports_usd,
            MAX(gdp_current_usd) AS gdp_current_usd,
			MAX(population_total) AS population_total,
			MAX(gdp_growth_annual_pct) AS gdp_growth_annual_pct,
			MAX(trade_pct_of_gdp) AS trade_pct_of_gdp,
            COUNT(DISTINCT partner_iso3) AS total_trade_partners,
			COUNT(DISTINCT commodity_code) AS total_commodities
		FROM 
			fact_global_trade_intelligence_dataset
		GROUP BY
			reporter_iso3,
            reporter_name,
            reference_year
	)
    SELECT
		reporter_iso3,
		reporter_name,
		reference_year,
        total_exports_usd,
		total_fob_exports_usd,
        gdp_current_usd,
		population_total,
		gdp_growth_annual_pct,
		trade_pct_of_gdp,
        total_trade_partners,
		total_commodities,
        RANK() OVER(PARTITION BY reference_year ORDER BY total_exports_usd DESC ) AS global_export_rank
	FROM 
    country_summary;


-- Creating view: vw_dashboard_dataset
-- This will serve as the primary Power BI dataset.
CREATE VIEW 
	vw_dashboard_dataset 
AS
WITH 
	dashboard_data 
    AS
    (
		SELECT
			reporter_iso3,
			reporter_name,
			reference_year,
            SUM(trade_value_usd) AS total_exports_usd,
            MAX(gdp_current_usd) AS gdp_current_usd,
			MAX(population_total) AS population_total,
			MAX(gdp_growth_annual_pct) AS gdp_growth_annual_pct,
			MAX(trade_pct_of_gdp) AS trade_pct_of_gdp
		FROM 
			fact_global_trade_intelligence_dataset
		GROUP BY
            reporter_iso3,
			reporter_name,
			reference_year
	)
		SELECT
			reporter_iso3,
			reporter_name,
			reference_year,
            total_exports_usd,
			gdp_current_usd,
			population_total,
			gdp_growth_annual_pct,
			trade_pct_of_gdp,
            RANK() OVER(PARTITION BY reference_year ORDER BY total_exports_usd DESC) AS global_export_rank,
            LAG(total_exports_usd) OVER(PARTITION BY reporter_iso3 ORDER BY reference_year) AS previous_year_exports,
            ROUND((total_exports_usd - LAG(total_exports_usd) OVER(PARTITION BY reporter_iso3 ORDER BY reference_year)) / 
				NULLIF(LAG(total_exports_usd) OVER(PARTITION BY reporter_iso3 ORDER BY reference_year), 0 ) * 100, 2 ) AS yoy_export_growth_pct
		FROM 
			dashboard_data;