# 16. Road Crashes across States

Which states record the highest crash burden and severity?

**Implementation status:** AWAITING_PRIMARY_DATA. Native Power BI and Tableau dashboards are pending desktop authoring and validation.

## Source and definitions
NBS/FRSC Road Transport Data

https://microdata.nigerianstat.gov.ng/index.php/catalog/164

Primary KPIs: Crashes; deaths; injuries; deaths per 100 crashes

Population rates are not travel-exposure rates. Counts depend on reporting and road usage.

## Execute
From the repository root:
```bash
python projects/16_road_crashes_across_states/python/run.py
```
The six WDI-enabled projects download national previews automatically. Other projects require a validated aggregate data/input.csv with the documented schema and a data/provenance.json declaring the transformations and original sources. No raw-survey mapping or automatic microdata extraction is claimed.

## Tool chain
Python downloads/validates data → SQLite executes sql/analysis.sql → outputs/analysis.csv feeds Excel, Power BI and Tableau. See notebooks/analysis.ipynb, excel/README.md, powerbi/BUILD.md and tableau/BUILD.md.

## Remaining primary-source work
Acquire the original source, verify variables/units/geographic coverage, implement and review source-specific transformation, estimate survey uncertainty where relevant, then author and validate native dashboards. The shared aggregate pipeline does not itself finish these substantive analyses.
