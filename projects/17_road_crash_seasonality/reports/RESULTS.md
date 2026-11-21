# Road Crash Seasonality: primary NBS analysis

Q1 2026 recorded 2,720 crashes, a +2.64% change from Q1 2025.

## Evidence and validation
22 quarters × 37 states/FCT = 814 state-quarter records. All eight state-count columns reconcile to source national totals in every quarter. Severity categories and casualty components reconcile for every state-quarter. The latest-quarter factor columns separately reconcile to published national totals. The adapter records source hashes and exact workbook rows.

## Methods
SQL is in sql/primary_analysis.sql. Source: https://microdata.nigerianstat.gov.ng/index.php/catalog/164/download/1405. Data tables and a balanced-period seasonality comparison are exported in outputs/.

![Primary chart](../outputs/trend.png)

## Limits
Only quarterly timing is observed. The balanced seasonality comparison uses 2021–2025, five complete years. No hour-of-day risk or prospective safety advice is inferred.

## Decision use
Use counts to select locations or periods for a more detailed reporting and exposure audit. Do not equate fewer reports with safer roads.

Native Power BI and Tableau authoring/validation is deferred to the user’s desktop session.
