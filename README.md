# Global Trade & Supply Chain Intelligence Platform

## Project Overview

This project demonstrates an end-to-end Data Analytics solution built using Python, MySQL, Microsoft Excel, and Power BI. The objective was to simulate a real-world analytics workflow by collecting trade and economic data from multiple public APIs, transforming it into analytics-ready datasets, designing a relational data warehouse, and developing interactive dashboards for business reporting.

The project combines international merchandise trade data from the United Nations Comtrade API with macroeconomic indicators from the World Bank API to create a unified analytical platform for global trade analysis.

Instead of importing CSV files directly into Power BI, this project follows an industry-oriented data analytics workflow consisting of data extraction, cleaning, database design, warehouse development, business view creation, Excel-based analysis, and interactive dashboard development.

---

# Business Problem

International trade data and macroeconomic indicators are available from multiple organizations but are often stored separately. This makes it difficult to analyze how exports relate to economic performance, GDP growth, population, and trade intensity.

The objective of this project is to integrate these datasets into a single analytical environment that enables users to:

- Analyze export performance across countries
- Compare countries over multiple years
- Evaluate economic indicators alongside trade performance
- Identify export growth trends
- Perform scenario and sensitivity analysis
- Build interactive dashboards for business decision-making

---

# Project Objectives

The primary objectives of this project are:

- Extract trade and economic data using REST APIs
- Perform data cleaning and validation using Python
- Build a structured MySQL data warehouse
- Create reusable analytical SQL views
- Develop Excel-based analytical models
- Build interactive Power BI dashboards
- Demonstrate an end-to-end Data Analytics workflow

---

# Dataset Information

## Data Sources

The project integrates data from the following public APIs:

| Source | Data Used |
|---------|-----------|
| UN Comtrade API | International Merchandise Trade |
| World Bank API | GDP, Population, GDP Growth, Trade (% of GDP) |

---

## Time Period

2015 – 2024

---

## Geographic Coverage

Global (Country-Level)

---

## Business Domain

International Trade Analytics

---

## Technologies Used

- Python
- Pandas
- Requests
- MySQL
- SQL
- Microsoft Excel
- Power BI
- Git
- GitHub

---

# Project Architecture

```text
                UN Comtrade API
                       │
                       │
               World Bank API
                       │
                       ▼
         Python Data Extraction Scripts
                       │
                       ▼
        Data Cleaning & Transformation
                       │
                       ▼
         Analytics-Ready CSV Datasets
                       │
                       ▼
            MySQL Data Warehouse
                       │
                       ▼
          Master Fact Table Creation
                       │
                       ▼
          Business Analytical Views
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
 Microsoft Excel              Power BI
 Executive Reports      Interactive Dashboards
```

---

# Project Workflow

The complete workflow implemented in this project consists of the following stages:

1. Data Collection
2. Data Cleaning
3. Data Transformation
4. Database Design
5. Data Loading
6. SQL Data Warehouse Development
7. Master Dataset Creation
8. Business View Development
9. Excel Reporting
10. Power BI Dashboard Development

---

# Repository Structure

```text
Global-Trade-Supply-Chain-Intelligence-Platform/
│
├── data/
│   ├── raw_data/
│   └── processed_data/
│
├── notebooks/
│
├── sql/
│
├── excel/
│
├── powerbi/
│
├── reports/
│
├── docs/
│
├── src/
│
├── assets/
│   ├── images/
│   ├── excel/
│   ├── powerbi/
│   └── sql/
│
├── requirements.txt
├── README.md
└── LICENSE
```

# ETL Process

The project follows a structured ETL (Extract, Transform, Load) workflow to convert raw API responses into analytics-ready datasets.

---

## Step 1: Data Extraction

Data was collected programmatically using Python by connecting to publicly available REST APIs.

### UN Comtrade API

Trade data was extracted for:

- Merchandise Exports
- Annual Frequency
- HS Classification
- Years: 2015–2024

### World Bank API

Macroeconomic indicators collected include:

- GDP (Current US$)
- Population
- GDP Growth (%)
- Trade (% of GDP)

The extracted datasets were stored separately as raw CSV files to preserve the original source data.

---

## Step 2: Data Cleaning & Transformation

The raw datasets were cleaned using Python before being loaded into MySQL.

Cleaning activities included:

- Data type conversion
- Duplicate validation
- Missing value handling
- Boolean conversion
- Date formatting
- Column standardization
- Country code validation
- Analytics-ready formatting

Separate cleaned datasets were generated for both UN Comtrade and World Bank data.

---

## Step 3: Data Validation

Before loading data into the database, several quality checks were performed.

Validation checks included:

- Row count verification
- Column count verification
- Duplicate record detection
- Missing value analysis
- Data type validation
- Country code consistency
- Year range verification

Only validated datasets were loaded into the SQL warehouse.

---

# Database Design

A relational database was designed in MySQL to store cleaned datasets and support analytical reporting.

The warehouse follows a simplified dimensional modeling approach where cleaned source datasets are stored individually before being merged into a master analytical table.

The database contains:

- Comtrade Fact Table
- World Bank Fact Table
- Master Trade Intelligence Table
- Analytical SQL Views

---

## Database Tables

### fact_comtrade_exports_dataset

Stores cleaned international trade data extracted from the UN Comtrade API.

Major attributes include:

- Reporter Country
- Partner Country
- Commodity
- Export Value
- FOB Value
- Trade Flow
- Classification
- Reporting Status

---

### fact_world_bank_dataset

Stores annual economic indicators collected from the World Bank API.

Major attributes include:

- GDP
- Population
- GDP Growth
- Trade (% of GDP)

Each record represents one country for one reporting year.

---

### fact_global_trade_intelligence_dataset

This table serves as the central analytical dataset for reporting.

It was created by joining the Comtrade and World Bank datasets using:

- reporter_iso3
- reference_year

The master table combines international trade statistics with economic indicators, enabling integrated business analysis.

---

# Data Warehouse Design

The warehouse was designed to separate raw source datasets from analytical reporting datasets.

Workflow:

```text
Comtrade Dataset
        │
        │
        ▼
fact_comtrade_exports_dataset
        │
        │
        ├──────────────┐
        │              │
        ▼              ▼
World Bank      fact_world_bank_dataset
        │              │
        └──────┬───────┘
               ▼
fact_global_trade_intelligence_dataset
               │
               ▼
      Business Analytical Views
```

---

# Indexing Strategy

Indexes were created on frequently queried columns to improve reporting performance.

Indexed columns include:

- reporter_iso3
- partner_iso3
- reference_year
- commodity_code

Benefits:

- Faster joins
- Faster filtering
- Improved aggregation performance
- Better dashboard responsiveness

---

# SQL Scripts Included

The SQL folder contains separate scripts for each stage of the database development process.

| SQL File | Purpose |
|----------|---------|
| Step_1_Database_Schema_Design.sql | Database and table creation |
| Step_2_Data_Loading.sql | CSV data loading |
| Step_3_Data_Validation.sql | Data quality validation |
| Create_Master_Fact_Table.sql | Master analytical table creation |
| Create_Views.sql | Business reporting views |

---

# Business Views Developed

Several reusable SQL views were created to simplify reporting and reduce repetitive SQL queries.

The project includes the following analytical views:

| View | Purpose |
|------|----------|
| vw_country_yearly_exports | Country-wise export summary |
| vw_partner_trade_analysis | Trade partner analysis |
| vw_top_exporting_countries | Global export ranking |
| vw_commodity_exports | Commodity-level export analysis |
| vw_trade_economic_profile | Trade and economic comparison |
| vw_trade_growth_indicators | Growth trend analysis |
| vw_country_trade_summary | Country performance summary |
| vw_dashboard_dataset | Power BI and Excel reporting dataset |
| vw_scenario_analysis_dataset | Scenario analysis dataset |

These views provide business-ready datasets that can be directly connected to Microsoft Excel and Power BI.

---

# SQL Concepts Demonstrated

The project demonstrates practical use of SQL for analytical reporting.

Topics covered include:

### Database Design

- Relational Database Design
- Primary Keys
- Unique Constraints
- Indexing

### Data Manipulation

- INNER JOIN
- LEFT JOIN
- GROUP BY
- ORDER BY
- Aggregate Functions

### Analytical SQL

- Common Table Expressions (CTEs)
- Window Functions
- RANK()
- LAG()
- CASE Statements

### Performance Optimization

- Index Creation
- Query Optimization
- View-Based Reporting

### Data Warehousing

- Fact Table Design
- Master Analytical Table
- Business Reporting Views

---

# Data Quality Measures

To improve data reliability, several validation rules were implemented throughout the ETL process.

These include:

- Consistent data types across datasets
- Standardized country codes (ISO-3)
- Duplicate prevention
- Boolean validation
- NULL value handling
- Referential consistency during dataset merging

These checks help ensure that downstream reports and dashboards are built on reliable and consistent data.

# Microsoft Excel Analysis

Microsoft Excel was used to create business-focused analytical reports before developing the final Power BI dashboards. Rather than using Excel only as a data viewing tool, the project demonstrates how Excel can be used for executive reporting, business analysis, and scenario planning.

The Excel workbooks were connected directly to MySQL analytical views, allowing reports to be refreshed whenever the underlying database is updated.

---

## Workbook 1: Executive Dashboard

The Executive Dashboard provides a high-level summary of global export performance and key economic indicators.

The workbook includes:

- Data Import from MySQL
- Data Quality Checks
- Pivot Table Analysis
- Executive Dashboard

The dashboard highlights:

- Total Exports
- GDP
- Population
- GDP Growth
- Trade (% of GDP)
- Global Export Rank
- Export Growth
- Year-wise Analysis

> Replace this section with your Excel Executive Dashboard screenshot.

![Excel Executive Dashboard](assets/excel/executive_dashboard.png)

---

## Workbook 2: Scenario Analysis

The Scenario Analysis workbook demonstrates how changes in economic assumptions affect export performance.

The workbook contains the following worksheets:

- Data Import
- Assumptions
- Scenario Model
- Sensitivity Analysis
- Dashboard

Business users can modify assumptions such as:

- Export Value
- GDP
- Population
- GDP Growth
- Trade (% of GDP)

The workbook automatically recalculates key performance indicators and visualizations based on the selected scenario.

This demonstrates practical use of Excel for business planning and what-if analysis.

> Replace this section with your Scenario Analysis Dashboard screenshot.

![Scenario Analysis Dashboard](assets/excel/scenario_analysis.png)

---

# Power BI Dashboard

Power BI was connected directly to MySQL using the analytical views created during the SQL development phase.

Instead of importing raw CSV files, the dashboards consume business-ready datasets prepared inside the SQL warehouse.

This approach improves performance, simplifies report development, and follows a workflow commonly used in industry.

The Power BI report focuses on answering business questions related to international trade, economic performance, and export growth.

---

## Dashboard Features

The Power BI solution includes interactive visualizations such as:

- KPI Cards
- Line Charts
- Bar Charts
- Maps
- Matrix Tables
- Trend Analysis
- Ranking Analysis
- Slicers
- Drill-down Reports

Users can filter reports by:

- Country
- Year
- Commodity
- Trade Partner

---

## Executive Dashboard

The Executive Dashboard provides a consolidated overview of global trade performance.

Key metrics displayed include:

- Total Exports
- GDP
- Population
- GDP Growth
- Trade (% of GDP)
- Global Export Rank
- Export Growth (%)

> Replace this section with your Executive Dashboard screenshot.

![Executive Dashboard](assets/powerbi/executive_dashboard.png)

---

## Trade Performance Dashboard

This dashboard focuses on country-level export analysis.

Business users can identify:

- Top Exporting Countries
- Export Growth Trends
- Country Rankings
- Historical Export Performance

> Replace this section with your Trade Dashboard screenshot.

![Trade Dashboard](assets/powerbi/trade_dashboard.png)

---

## Economic Indicators Dashboard

This dashboard combines trade statistics with macroeconomic indicators.

It enables comparison of:

- GDP vs Exports
- GDP Growth vs Export Growth
- Population vs Export Performance
- Trade (% of GDP)

> Replace this section with your Economic Dashboard screenshot.

![Economic Dashboard](assets/powerbi/economic_dashboard.png)

---

# Business KPIs Developed

The project enables analysis of several important business metrics.

### Trade Performance

- Total Exports
- Previous Year Exports
- Export Growth (%)
- Global Export Rank

### Economic Indicators

- GDP
- GDP Growth (%)
- Population
- Trade (% of GDP)

### Productivity Metrics

- Export per Capita
- GDP per Capita
- Export to GDP Ratio

### Trend Analysis

- Year-over-Year Export Growth
- Country Performance
- Economic Growth Trends

---

# Project Deliverables

The repository contains the following deliverables:

| Deliverable | Description |
|-------------|-------------|
| Python Scripts | Data extraction, cleaning, and transformation |
| Processed Datasets | Analytics-ready CSV files |
| SQL Scripts | Database design, data loading, validation, warehouse development, and analytical views |
| MySQL Data Warehouse | Structured analytical database |
| Excel Workbook 1 | Executive Dashboard |
| Excel Workbook 2 | Scenario Analysis |
| Power BI Dashboard | Interactive business intelligence reports |
| Documentation | Business Problem, ETL Process, Data Model, Final Report |

---

# Key Skills Demonstrated

This project demonstrates practical experience in the following areas:

### Python

- REST API Integration
- Data Extraction
- Data Cleaning
- Data Transformation
- ETL Pipeline Development
- Data Validation

### SQL & MySQL

- Relational Database Design
- Data Warehousing
- SQL Query Development
- Window Functions
- Common Table Expressions (CTEs)
- Indexing
- Analytical Views
- Query Optimization

### Microsoft Excel

- Data Import from SQL
- Pivot Tables
- Pivot Charts
- Dashboard Design
- Scenario Analysis
- Sensitivity Analysis
- Business Reporting

### Power BI

- Data Modeling
- DAX Measures
- KPI Development
- Interactive Dashboards
- Business Intelligence Reporting
- Data Visualization

---

# Business Value

This project demonstrates how multiple public datasets can be integrated into a unified analytical platform to support business decision-making.

The solution enables users to:

- Monitor export performance across countries
- Compare trade trends over time
- Analyze economic indicators alongside trade data
- Perform scenario and sensitivity analysis
- Support data-driven business decisions

The overall workflow closely follows a real-world analytics project, beginning with API data extraction and ending with interactive dashboards for business users.


# Project Structure

```text
Global-Trade-Supply-Chain-Intelligence/
│
├── data/
│   ├── raw_data/
│   └── processed_data/
│
├── notebooks/
│   ├── extract_comtrade_data.ipynb
│   ├── clean_comtrade_data.ipynb
│   ├── extract_world_bank_data.ipynb
│   └── clean_world_bank_data.ipynb
│
├── python/
│   ├── config.py
│   ├── load_data_to_mysql.py
│   └── merge_datasets.py
│
├── sql/
│   ├── Step_1_Database_Schema_Design.sql
│   ├── Step_2_Data_Loading.sql
│   ├── Step_3_Data_Validation.sql
│   ├── Create_Master_Fact_Table.sql
│   ├── Create_Views.sql
│   └── Create_Indexes.sql
│
├── excel/
│   ├── 01_Executive_Dashboard.xlsx
│   └── 02_Scenario_Analysis.xlsx
│
├── powerbi/
│   └── Global_Trade_Supply_Chain_Intelligence.pbix
│
├── documentation/
│   ├── Business_Problem.md
│   ├── Data_Model.md
│   ├── ETL_Process.md
│   └── Final_Report.pdf
│
├── assets/
│   ├── excel/
│   ├── powerbi/
│   └── database/
│
├── requirements.txt
└── README.md
```

---

# How to Run the Project

To reproduce this project locally, follow the steps below.

## Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/Global-Trade-Supply-Chain-Intelligence.git
```

Move into the project directory.

```bash
cd Global-Trade-Supply-Chain-Intelligence
```

---

## Step 2: Install Python Dependencies

Install all required Python libraries using:

```bash
pip install -r requirements.txt
```

---

## Step 3: Extract the Data

Run the notebooks to download data from the APIs.

Execution order:

1. extract_comtrade_data.ipynb
2. clean_comtrade_data.ipynb
3. extract_world_bank_data.ipynb
4. clean_world_bank_data.ipynb

These notebooks will generate analytics-ready CSV files inside the `processed_data` folder.

---

## Step 4: Create the MySQL Database

Execute the SQL scripts in the following order.

1. Step_1_Database_Schema_Design.sql
2. Step_2_Data_Loading.sql
3. Step_3_Data_Validation.sql
4. Create_Master_Fact_Table.sql
5. Create_Indexes.sql
6. Create_Views.sql

After completing these steps, the data warehouse and analytical views will be ready for reporting.

---

## Step 5: Open the Excel Workbooks

Open the following workbooks:

- 01_Executive_Dashboard.xlsx
- 02_Scenario_Analysis.xlsx

Refresh the SQL connections to load the latest data from MySQL.

---

## Step 6: Open the Power BI Report

Open the Power BI report.

```
Global_Trade_Supply_Chain_Intelligence.pbix
```

Refresh the data source connection to load the latest information from the MySQL database.

---

# Future Enhancements

Several improvements can be incorporated into future versions of this project.

Potential enhancements include:

- Import and analyze both Imports and Exports instead of only Exports.
- Integrate additional datasets from the WTO or IMF for richer economic analysis.
- Automate the complete ETL pipeline using scheduled workflows.
- Deploy the MySQL database to a cloud platform.
- Publish the Power BI report using the Power BI Service.
- Add forecasting models using Python.
- Incorporate machine learning models for export prediction.
- Build a web application for interactive dashboard access.

---

# Learning Outcomes

Working on this project provided practical experience in building a complete analytics solution from raw data collection to business reporting.

Key areas of learning include:

- Working with REST APIs to collect large datasets.
- Cleaning and transforming real-world data using Python.
- Designing relational databases in MySQL.
- Building a structured analytical data warehouse.
- Creating optimized SQL queries and analytical views.
- Implementing indexing for better query performance.
- Combining trade and economic datasets for integrated analysis.
- Developing business-focused Excel reports and scenario analysis models.
- Designing interactive Power BI dashboards for business users.
- Translating business requirements into analytical solutions.

---

# References

The following public data sources were used in this project.

### UN Comtrade

- International merchandise trade statistics
- HS Commodity Classification
- Annual Trade Data

### World Bank Open Data

- GDP (Current US$)
- Population
- GDP Growth
- Trade (% of GDP)

These datasets are publicly available and were accessed through their respective APIs.

---

# Author

**Mohammad Wasiq Khan**

Data Analyst | SQL | Python | Power BI | Microsoft Excel

This project was developed as part of my data analytics portfolio to demonstrate practical skills in data engineering, SQL development, business intelligence, and dashboard design using real-world international trade and economic datasets.

---

# Acknowledgements

I would like to acknowledge the organizations that provide open access to high-quality public datasets used in this project.

- United Nations Comtrade Database
- World Bank Open Data

Their publicly available APIs make it possible to build practical analytics projects using real-world data.

---

If you found this project helpful or interesting, feel free to explore the repository, provide feedback, or connect with me on LinkedIn.