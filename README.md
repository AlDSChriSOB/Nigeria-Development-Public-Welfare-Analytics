# Nigeria Development and Public Welfare Analytics

20 Nigerian case studies integrating Excel, SQLite SQL, Python/Jupyter, Power BI and Tableau.

**This release implements the project structure and aggregate-indicator workflow. It does not claim 20 completed end-to-end studies.** Six projects have executed national-data previews. Projects 16–17 now have verified primary NBS analyses; project 18 has primary factor distributions but lacks linked factor-by-severity records. Eleven projects still await primary data and source-specific transformations. No native Power BI or Tableau dashboards have yet been authored or validated. No synthetic analysis data was used.

## Quick start
```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run_all.py
```
Internet access is needed for first-time WDI downloads. A project awaiting primary data returns AWAITING_PRIMARY_DATA, never fabricated results. STATUS.json lists each outcome. Failed downloads cause a nonzero run_all.py exit.

## How the tools work together
| Tool | Implemented role | Remaining work |
|---|---|---|
| Python | WDI downloader, validation, SQLite execution, provenance, charts, CSV exports | Original-source mappings for surveys, NBS and security data |
| SQL | Unique-key checks and previous-observation changes within geography, metric, unit and vintage | Case-specific models and derived indicators after source inspection |
| Jupyter | Executable workflow and source/interpretation notes for every project | Primary-case interpretation and survey uncertainty |
| Excel | Twenty actual XLSX workbooks; six populated national previews, three primary NBS workbooks and eleven explicit no-data workbooks; Power Query scripts | Native Excel refresh validation and primary-data population |
| Power BI | Twenty Power Query imports, DAX measures, themes and dashboard build specifications | Native reports, desktop validation and service publication |
| Tableau | Twenty data connection, calculation and dashboard build specifications | Native workbooks, desktop validation and service publication |

## Directories
Each projects/NN_case directory contains data/, excel/, sql/, python/, notebooks/, powerbi/, tableau/, reports/ and outputs/.

## Project catalogue
| # | Case study | Current data scope |
|---|---|---|
| 01 | [GDP and Economic Diversification](projects/01_gdp_and_economic_diversification/README.md) | Executed national preview |
| 02 | [Growth and Household Welfare](projects/02_growth_and_household_welfare/README.md) | Awaiting primary data |
| 03 | [Food Prices and Purchasing Power](projects/03_food_prices_and_purchasing_power/README.md) | Awaiting primary data |
| 04 | [Petrol and Transport Costs](projects/04_petrol_and_transport_costs/README.md) | Awaiting primary data |
| 05 | [Security and Civilian Exposure](projects/05_security_and_civilian_exposure/README.md) | Awaiting primary data |
| 06 | [Insecurity and Agricultural Activity](projects/06_insecurity_and_agricultural_activity/README.md) | Awaiting primary data |
| 07 | [Security and Business Constraints](projects/07_security_and_business_constraints/README.md) | Awaiting primary data |
| 08 | [Crop Production and Yield](projects/08_crop_production_and_yield/README.md) | Executed national preview |
| 09 | [Inputs Irrigation and Productivity](projects/09_inputs_irrigation_and_productivity/README.md) | Awaiting primary data |
| 10 | [Storage and Market Access](projects/10_storage_and_market_access/README.md) | Awaiting primary data |
| 11 | [Rural Infrastructure and Welfare](projects/11_rural_infrastructure_and_welfare/README.md) | Awaiting primary data |
| 12 | [Electricity and Economic Opportunity](projects/12_electricity_and_economic_opportunity/README.md) | Executed national preview |
| 13 | [Water Sanitation and Inequality](projects/13_water_sanitation_and_inequality/README.md) | Executed national preview |
| 14 | [Government Policy and Approval](projects/14_government_policy_and_approval/README.md) | Awaiting primary data |
| 15 | [Public Mood and Confidence](projects/15_public_mood_and_confidence/README.md) | Awaiting primary data |
| 16 | [Road Crashes across States](projects/16_road_crashes_across_states/README.md) | Primary NBS analysis |
| 17 | [Road Crash Seasonality](projects/17_road_crash_seasonality/README.md) | Primary NBS analysis |
| 18 | [Crash Severity and Contributing Factors](projects/18_crash_severity_and_contributing_factors/README.md) | Primary NBS analysis (partial question) |
| 19 | [Healthcare and Financial Barriers](projects/19_healthcare_and_financial_barriers/README.md) | Executed national preview |
| 20 | [Maternal and Child Healthcare](projects/20_maternal_and_child_healthcare/README.md) | Executed national preview |

## Data and interpretation
National WDI indicators are initial context, not substitutes for the proposed state or household case studies. Six national previews cover GDP structure, cereal production/yield, electricity, water/sanitation, health financing and maternal/child health. Geographic comparisons require matching time coverage, definitions and denominators. GHS-Panel and Afrobarometer must not automatically be treated as state-representative. Survey-based outputs require explicit eligible-population coding and design-based uncertainty outside this aggregate pipeline.

Raw or restricted data and credentials are excluded. Download instructions and original-source links accompany every case. Honour provider access and redistribution terms. Do not publish respondent-level health or political-opinion data in this repository.

## Excel build
The supplied XLSX files open independently. Power Query imports can load the CSV output in Excel. The original workbook builder uses @oai/artifact-tool in the Codex runtime and is not a standard pip dependency. scripts/build_excel.mjs records the build procedure; regenerating XLSX through that builder requires the same runtime or adapting it to your licensed local environment. The standard Python pipeline does not regenerate XLSX automatically.

## Publication status
Published to https://github.com/AlDSChriSOB/Nigeria-Development-Public-Welfare-Analytics on 21 November 2026. All 20 case-study directories are included. Publication does not mean the primary studies or native BI dashboards are complete.

## Definition of completion
A case is complete only after primary-source acquisition and mapping, analysis and uncertainty checks, Excel reconciliation, native BI dashboard authoring/validation, reviewed findings, reproducibility checks and publication. Current progress is reported without treating missing-data templates or passing code execution as substantive completion.
