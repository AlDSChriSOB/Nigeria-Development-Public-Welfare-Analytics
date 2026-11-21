# 04. Petrol and Transport Costs

How do fuel and passenger-fare changes co-move?

**Implementation status:** AWAITING_PRIMARY_DATA. Native Power BI and Tableau dashboards are pending desktop authoring and validation.

## Source and definitions
NBS Petrol Price Watch and Transport Fare Watch

https://www.nigerianstat.gov.ng/elibrary

Primary KPIs: NGN per litre; fare by transport mode

Align state-month-mode keys. Price co-movement does not identify subsidy effects.

## Execute
From the repository root:
```bash
python projects/04_petrol_and_transport_costs/python/run.py
```
The six WDI-enabled projects download national previews automatically. Other projects require a validated aggregate data/input.csv with the documented schema and a data/provenance.json declaring the transformations and original sources. No raw-survey mapping or automatic microdata extraction is claimed.

## Tool chain
Python downloads/validates data → SQLite executes sql/analysis.sql → outputs/analysis.csv feeds Excel, Power BI and Tableau. See notebooks/analysis.ipynb, excel/README.md, powerbi/BUILD.md and tableau/BUILD.md.

## Remaining primary-source work
Acquire the original source, verify variables/units/geographic coverage, implement and review source-specific transformation, estimate survey uncertainty where relevant, then author and validate native dashboards. The shared aggregate pipeline does not itself finish these substantive analyses.
