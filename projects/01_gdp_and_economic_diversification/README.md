# 01. GDP and Economic Diversification

Which sectors account for output and how has real GDP changed?

**Implementation status:** NATIONAL_PREVIEW_READY. Native Power BI and Tableau dashboards are pending desktop authoring and validation.

## Source and definitions
NBS GDP tables; World Bank WDI national preview

https://microdata.nigerianstat.gov.ng/index.php/catalog/147

Primary KPIs: Sector shares and real GDP growth

Do not splice GDP vintages or confuse nominal value added shares with real growth.

## Execute
From the repository root:
```bash
python projects/01_gdp_and_economic_diversification/python/run.py
```
The six WDI-enabled projects download national previews automatically. Other projects require a validated aggregate data/input.csv with the documented schema and a data/provenance.json declaring the transformations and original sources. No raw-survey mapping or automatic microdata extraction is claimed.

## Tool chain
Python downloads/validates data → SQLite executes sql/analysis.sql → outputs/analysis.csv feeds Excel, Power BI and Tableau. See notebooks/analysis.ipynb, excel/README.md, powerbi/BUILD.md and tableau/BUILD.md.

## Remaining primary-source work
Acquire the original source, verify variables/units/geographic coverage, implement and review source-specific transformation, estimate survey uncertainty where relevant, then author and validate native dashboards. The shared aggregate pipeline does not itself finish these substantive analyses.
