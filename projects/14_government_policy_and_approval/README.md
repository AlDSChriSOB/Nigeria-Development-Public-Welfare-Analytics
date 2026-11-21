# 14. Government Policy and Approval

How do Nigerians assess policies and government performance?

**Implementation status:** AWAITING_PRIMARY_DATA. Native Power BI and Tableau dashboards are pending desktop authoring and validation.

## Source and definitions
Afrobarometer Nigeria Round 10

https://www.afrobarometer.org/survey-resource/nigeria-round-10-data-2024/

Primary KPIs: Weighted approval by policy and demographic group

Verify question wording, coding, eligible denominator and sample design; approval is not policy impact.

## Execute
From the repository root:
```bash
python projects/14_government_policy_and_approval/python/run.py
```
The six WDI-enabled projects download national previews automatically. Other projects require a validated aggregate data/input.csv with the documented schema and a data/provenance.json declaring the transformations and original sources. No raw-survey mapping or automatic microdata extraction is claimed.

## Tool chain
Python downloads/validates data → SQLite executes sql/analysis.sql → outputs/analysis.csv feeds Excel, Power BI and Tableau. See notebooks/analysis.ipynb, excel/README.md, powerbi/BUILD.md and tableau/BUILD.md.

## Remaining primary-source work
Acquire the original source, verify variables/units/geographic coverage, implement and review source-specific transformation, estimate survey uncertainty where relevant, then author and validate native dashboards. The shared aggregate pipeline does not itself finish these substantive analyses.
