# 12. Electricity and Economic Opportunity

How does electricity access relate to work and enterprise activity?

**Implementation status:** NATIONAL_PREVIEW_READY. Native Power BI and Tableau dashboards are pending desktop authoring and validation.

## Source and definitions
Afrobarometer; GHS-Panel; WDI access preview

https://data.worldbank.org/country/nigeria

Primary KPIs: Access proportion; reliability; enterprise outcomes

National WDI access does not measure reliability or identify enterprise effects.

## Execute
From the repository root:
```bash
python projects/12_electricity_and_economic_opportunity/python/run.py
```
The six WDI-enabled projects download national previews automatically. Other projects require a validated aggregate data/input.csv with the documented schema and a data/provenance.json declaring the transformations and original sources. No raw-survey mapping or automatic microdata extraction is claimed.

## Tool chain
Python downloads/validates data → SQLite executes sql/analysis.sql → outputs/analysis.csv feeds Excel, Power BI and Tableau. See notebooks/analysis.ipynb, excel/README.md, powerbi/BUILD.md and tableau/BUILD.md.

## Remaining primary-source work
Acquire the original source, verify variables/units/geographic coverage, implement and review source-specific transformation, estimate survey uncertainty where relevant, then author and validate native dashboards. The shared aggregate pipeline does not itself finish these substantive analyses.
