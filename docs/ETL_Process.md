# ETL Process

# Overview

The **Global Trade & Supply Chain Intelligence Platform** follows a structured **Extract, Transform, Load (ETL)** pipeline to collect, clean, integrate, and analyze international trade and macroeconomic data.

The objective of the ETL process is to transform raw data from multiple public APIs into a centralized, analytics-ready data warehouse that supports reporting, business intelligence, and scenario analysis.

The complete workflow is designed to simulate a real-world data analytics pipeline commonly used in industry.

---

# ETL Architecture

```text
                Public APIs
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
UN Comtrade API           World Bank API
        │                         │
        └────────────┬────────────┘
                     ▼
            Python Extraction Scripts
                     │
                     ▼
               Raw CSV Files
                     │
                     ▼
      Python Cleaning & Transformation
                     │
                     ▼
          Processed Analytics-Ready CSVs
                     │
                     ▼
          MySQL Data Warehouse Loading
                     │
                     ▼
        Master Analytical Dataset Creation
                     │
                     ▼
           SQL Views for Reporting
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
 Microsoft Excel          Power BI Dashboards
```

---

# Phase 1 – Extract

## Objective

The extraction phase retrieves raw data from publicly available APIs.

Two different APIs are used in this project:

| Source                      | Data Collected                              |
| --------------------------- | ------------------------------------------- |
| United Nations Comtrade API | International export trade data             |
| World Bank API              | GDP, Population, GDP Growth, Trade % of GDP |

---

## UN Comtrade API Extraction

Trade data is downloaded using Python.

The extraction process includes:

* API authentication
* Batch data extraction
* Pagination handling
* API rate limit handling
* Automatic retries for failed requests
* Exporting responses into CSV files

The extracted dataset contains information such as:

* Reporter Country
* Partner Country
* Commodity
* Trade Value
* FOB Value
* Trade Flow
* Classification
* Reporting Year

---

## World Bank API Extraction

Macroeconomic indicators are downloaded separately.

The project retrieves:

* GDP (Current US$)
* Population
* GDP Growth (%)
* Trade (% of GDP)

Each indicator is extracted for multiple countries across multiple years.

---

# Phase 2 – Raw Data Storage

The extracted API responses are stored without modification.

Purpose:

* Preserve original data
* Allow reprocessing without calling APIs again
* Enable auditing
* Maintain reproducibility

Project Structure

```text
data/
│
├── raw_data/
│   ├── comtrade/
│   └── world_bank/
```

No transformations are performed at this stage.

---

# Phase 3 – Data Cleaning

After extraction, Python notebooks clean the raw datasets.

The cleaning process includes:

* Removing duplicate records
* Correcting data types
* Standardizing country codes
* Standardizing commodity codes
* Handling missing values
* Removing unnecessary columns
* Renaming columns
* Creating derived columns
* Validating exported records

Example transformations include:

* Converting year columns to integers
* Converting Boolean flags
* Standardizing ISO country codes
* Parsing timestamps
* Converting numeric fields to appropriate data types

The cleaned datasets become analytics-ready.

---

# Phase 4 – Data Validation

Before loading data into MySQL, several validation checks are performed.

Examples include:

* Duplicate record detection
* Missing value analysis
* Invalid country code detection
* Invalid commodity code detection
* Data type verification
* Record count verification
* Null value analysis

Validation ensures high-quality data enters the warehouse.

---

# Phase 5 – Load

The cleaned datasets are loaded into MySQL.

Two source tables are created.

## fact_comtrade_exports_dataset

Stores export trade records.

## fact_world_bank_dataset

Stores macroeconomic indicators.

Loading is performed using MySQL bulk import operations after the processed CSV files are generated.

Indexes and constraints are created to improve performance and maintain data integrity.

---

# Phase 6 – Data Integration

Once both datasets are available in MySQL, they are merged into a centralized analytical table.

Merge Keys

* reporter_iso3
* reference_year

Join Type

```sql
LEFT JOIN
```

The Comtrade dataset acts as the primary dataset.

Economic indicators are appended wherever matching country-year combinations exist.

The integrated dataset is stored as:

```text
fact_global_trade_intelligence_dataset
```

This table serves as the central source for all downstream reporting.

---

# Phase 7 – Analytical Views

Instead of querying the master table directly, multiple SQL views are created.

These views simplify reporting and improve reusability.

Views created in this project:

* vw_country_yearly_exports
* vw_partner_trade_analysis
* vw_top_exporting_countries
* vw_commodity_exports
* vw_trade_economic_profile
* vw_trade_growth_indicators
* vw_country_trade_summary
* vw_dashboard_dataset
* vw_scenario_analysis_dataset

Each view is designed for a specific analytical purpose.

---

# Phase 8 – Microsoft Excel Reporting

Excel connects directly to MySQL and imports reporting datasets from SQL views.

Two workbooks are developed.

## Executive Dashboard

Provides executive-level reporting including:

* KPI Cards
* Pivot Tables
* Interactive Charts
* Country Comparisons
* Export Trends

---

## Scenario Analysis

Allows users to perform what-if analysis by changing assumptions.

Users can evaluate the impact of changes in:

* Exports
* GDP
* Population

Sensitivity analysis automatically updates calculations and charts.

---

# Phase 9 – Power BI Reporting

Power BI connects to MySQL using SQL views.

Interactive dashboards provide:

* Export Trends
* Country Rankings
* Economic Indicators
* Trade Growth Analysis
* Geographic Analysis
* Executive KPIs
* Drill-through Analysis
* Interactive Filtering

Power BI becomes the primary business intelligence layer of the project.

---

# Data Quality Measures

Several quality checks are implemented throughout the pipeline.

These include:

* Data type validation
* Duplicate removal
* Missing value handling
* Boolean value standardization
* ISO country code validation
* Primary Key constraints
* Unique constraints
* SQL indexing
* Referential consistency during data integration

These checks improve reliability and reporting accuracy.

---

# Tools Used in the ETL Pipeline

| Stage                 | Technology       |
| --------------------- | ---------------- |
| Data Extraction       | Python           |
| API Integration       | Requests Library |
| Data Cleaning         | Pandas           |
| Data Validation       | Pandas           |
| Data Storage          | CSV              |
| Data Warehouse        | MySQL            |
| SQL Development       | MySQL Workbench  |
| Business Reporting    | Microsoft Excel  |
| Dashboard Development | Power BI         |
| Version Control       | Git & GitHub     |

---

# Benefits of the ETL Design

This ETL pipeline provides several advantages:

* Automated data collection from multiple APIs.
* Repeatable and reusable data processing workflow.
* Separation of raw and processed datasets.
* Centralized analytical data warehouse.
* Improved data quality through validation and cleaning.
* Optimized SQL views for reporting.
* Easy integration with Excel and Power BI.
* Scalable architecture that can be extended with additional data sources.

---

# End-to-End ETL Workflow

```text
UN Comtrade API
        │
        ▼
Python Extraction
        │
        ▼
Raw CSV
        │
        ▼
Python Cleaning
        │
        ▼
Processed CSV
        │
        ├────────────────────┐
        ▼                    ▼
World Bank API        Python Extraction
                             │
                             ▼
                        Raw CSV
                             │
                             ▼
                      Python Cleaning
                             │
                             ▼
                     Processed CSV
                             │
                             ▼
                 MySQL Source Tables
                             │
                             ▼
          fact_global_trade_intelligence_dataset
                             │
                             ▼
                     SQL Analytical Views
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
      Microsoft Excel                 Power BI
```

---

# Conclusion

The ETL pipeline developed for this project demonstrates a complete end-to-end analytics workflow, beginning with automated data extraction from multiple public APIs and ending with interactive business intelligence dashboards. By combining Python for extraction and transformation, MySQL for data warehousing, Microsoft Excel for scenario analysis, and Power BI for visualization, the pipeline reflects industry-standard data engineering and analytics practices. The modular design ensures that new data can be processed efficiently while maintaining data quality, consistency, and scalability for future enhancements.