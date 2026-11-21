# 20. Maternal and Child Healthcare

Where are maternal-care and child-vaccination gaps largest?

**Implementation status:** NATIONAL_PREVIEW_READY. Native Power BI and Tableau dashboards are pending desktop authoring and validation.

## Source and definitions
NDHS 2024; WDI national preview

https://microdata.worldbank.org/catalog/8029

Primary KPIs: Skilled birth attendance; child immunisation

WDI national trends do not fulfil state or demographic inequalities; denominator populations differ by indicator.

## Execute
From the repository root:
```bash
python projects/20_maternal_and_child_healthcare/python/run.py
```
The six WDI-enabled projects download national previews automatically. Other projects require a validated aggregate data/input.csv with the documented schema and a data/provenance.json declaring the transformations and original sources. No raw-survey mapping or automatic microdata extraction is claimed.

## Tool chain
Python downloads/validates data → SQLite executes sql/analysis.sql → outputs/analysis.csv feeds Excel, Power BI and Tableau. See notebooks/analysis.ipynb, excel/README.md, powerbi/BUILD.md and tableau/BUILD.md.

## Remaining primary-source work
Acquire the original source, verify variables/units/geographic coverage, implement and review source-specific transformation, estimate survey uncertainty where relevant, then author and validate native dashboards. The shared aggregate pipeline does not itself finish these substantive analyses.
