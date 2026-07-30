# Data Model

## Overview

The **Global Trade & Supply Chain Intelligence Platform** uses a relational analytical data model designed to support business intelligence, reporting, and dashboard development.

The project integrates international trade data from the **United Nations Comtrade API** with macroeconomic indicators from the **World Bank API**. These datasets are stored in a MySQL data warehouse and combined into a centralized analytical table to simplify reporting and analysis.

The data model follows a reporting-oriented design where cleaned datasets are first stored individually and then merged into a master analytical dataset. SQL views are created on top of this master table to provide optimized datasets for Microsoft Excel and Power BI dashboards.

---

# Data Sources

The project integrates data from the following public data sources:

| Data Source                 | Purpose                                     |
| --------------------------- | ------------------------------------------- |
| United Nations Comtrade API | International export trade statistics       |
| World Bank API              | GDP, Population, GDP Growth, Trade % of GDP |

---

# Database Architecture

The database consists of four logical layers.

```
Raw API Data
        │
        ▼
Python Data Cleaning & Transformation
        │
        ▼
MySQL Database
        │
        ├───────────────┐
        │               │
        ▼               ▼
fact_comtrade_exports_dataset
fact_world_bank_dataset
        │
        └───────────────┐
                        ▼
fact_global_trade_intelligence_dataset
                        │
                        ▼
Analytical SQL Views
                        │
                        ▼
Excel & Power BI Dashboards
```

---

# Database Tables

The project contains three primary tables.

## 1. fact_comtrade_exports_dataset

This table stores cleaned export trade records downloaded from the UN Comtrade API.

Each record represents exports for:

* One Reporter Country
* One Partner Country
* One Commodity
* One Year

### Primary Key

```
comtrade_fact_id
```

### Main Attributes

* Reporter Country
* Partner Country
* Commodity
* Trade Value
* FOB Value
* Trade Flow
* Classification
* Download Timestamp

---

## 2. fact_world_bank_dataset

This table stores country-level macroeconomic indicators downloaded from the World Bank API.

Each record represents one country for one year.

### Primary Key

```
wb_fact_id
```

### Unique Constraint

```
(reporter_iso3, reference_year)
```

### Main Attributes

* GDP
* Population
* GDP Growth
* Trade % of GDP

---

## 3. fact_global_trade_intelligence_dataset

This is the central analytical table of the project.

It is created by joining:

```
fact_comtrade_exports_dataset

INNER JOIN

fact_world_bank_dataset
```

using

```
reporter_iso3
reference_year
```

This table combines trade data and economic indicators into a single analytics-ready dataset.

It is the primary source for reporting, Excel models, and Power BI dashboards.

---

# Join Logic

The datasets are merged using the following business keys.

| Comtrade       | World Bank     |
| -------------- | -------------- |
| reporter_iso3  | reporter_iso3  |
| reference_year | reference_year |

Join Type

```
LEFT JOIN
```

The Comtrade dataset is treated as the primary dataset because every export record should be preserved, even if some economic indicators are unavailable for a particular country and year.

---

# Entity Relationship

```
                     +-----------------------------+
                     | fact_world_bank_dataset     |
                     +-----------------------------+
                     | wb_fact_id (PK)             |
                     | reporter_iso3              |
                     | reference_year             |
                     | GDP                        |
                     | Population                 |
                     | GDP Growth                 |
                     | Trade % of GDP             |
                     +-------------▲--------------+
                                   │
                                   │
                                   │
                     reporter_iso3 + reference_year
                                   │
                                   │
                                   ▼
+--------------------------------------------------------------+
| fact_comtrade_exports_dataset                                |
+--------------------------------------------------------------+
| comtrade_fact_id (PK)                                        |
| reporter_iso3                                                |
| partner_iso3                                                 |
| commodity_code                                               |
| trade_value_usd                                              |
| fob_value_usd                                                |
| reference_year                                               |
+---------------------------┬----------------------------------+
                            │
                            ▼
+--------------------------------------------------------------+
| fact_global_trade_intelligence_dataset                       |
+--------------------------------------------------------------+
| Combined Trade + Economic Indicators                         |
+--------------------------------------------------------------+
```

---

# Analytical Views

Instead of querying the master table directly, the project uses SQL views for reporting.

| View                         | Purpose                                |
| ---------------------------- | -------------------------------------- |
| vw_country_yearly_exports    | Country-wise yearly exports            |
| vw_partner_trade_analysis    | Partner country analysis               |
| vw_top_exporting_countries   | Global export rankings                 |
| vw_commodity_exports         | Commodity-level exports                |
| vw_trade_economic_profile    | Trade vs economic indicators           |
| vw_trade_growth_indicators   | Export growth analysis                 |
| vw_country_trade_summary     | Country summary statistics             |
| vw_dashboard_dataset         | Optimized dataset for Excel & Power BI |
| vw_scenario_analysis_dataset | Dataset for Excel scenario modeling    |

Using views keeps dashboards simple while hiding SQL complexity from reporting tools.

---

# Why a Central Analytical Table?

Instead of joining tables repeatedly inside Power BI or Excel, the project creates a master analytical table.

Benefits include:

* Faster dashboard performance
* Simpler SQL queries
* Easier maintenance
* Reduced data duplication
* Consistent business logic
* Reusable analytical views

---

# Data Granularity

Understanding the level of detail is important for accurate analysis.

### Comtrade Dataset

One row represents:

```
Reporter Country
+
Partner Country
+
Commodity
+
Year
```

---

### World Bank Dataset

One row represents:

```
Reporter Country
+
Year
```

---

### Master Dataset

One row represents:

```
Reporter Country
+
Partner Country
+
Commodity
+
Year
+
Economic Indicators
```

---

# Data Flow

The project follows a structured ETL workflow.

```
Public APIs
     │
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
Processed CSV Files
     │
     ▼
MySQL Data Warehouse
     │
     ▼
Master Analytical Dataset
     │
     ▼
SQL Views
     │
     ├──────────────┐
     ▼              ▼
Microsoft Excel   Power BI
```

---

# Design Decisions

The following design choices were made during development:

* Python was used for API extraction, cleaning, and transformation.
* MySQL serves as the analytical data warehouse.
* Individual source datasets are stored separately before integration.
* Economic indicators are merged using standardized ISO country codes and reporting years.
* SQL views provide reporting-ready datasets for downstream tools.
* Excel is used for executive reporting and scenario analysis.
* Power BI is used for interactive dashboards and business intelligence reporting.

---

# Conclusion

The data model is designed to support scalable analytics by integrating multiple public datasets into a centralized analytical warehouse. By separating raw source tables, creating a unified master dataset, and exposing curated SQL views for reporting, the model simplifies downstream analysis while maintaining consistency, performance, and reusability across Microsoft Excel and Power BI.