# Water Sanitation and Inequality: native BI build and validation

Status: integration assets implemented; native dashboard NOT built or validated.

Decision: Who lacks basic water and sanitation services?
Indicators: Basic water and sanitation access

1. Run the Python pipeline. It executes SQLite and writes outputs/analysis.csv. Do not load data/input_contract.csv as actual observations.
2. In Power BI Desktop, create a blank query using ImportAnalysis.pq; set its CsvPath. Name it Analysis. Create measures from measures.dax individually and import theme.json.
3. In Tableau Desktop/Public, connect to outputs/analysis.csv as a text file. Set period to Date, value/change columns to Number, and geography/metric/unit/vintage to dimensions.
4. Create an overview with selected metric, latest observed value, period and vintage. Create a trend with period on Columns and value on Rows, filtered to one metric/unit/vintage; use geography for comparison only when definitions match.
5. Add a detail table for absolute_change and previous_period. Add a source-and-quality page showing the source, data grain and excluded/missing counts.
6. Set single-select metric/unit/vintage filters, date range, tooltips including unit/source, and a reset-filter button. Disable cross-indicator totals and misleading map layers. National previews have no state map.
7. Reconcile a selected period/geography against outputs/analysis.csv and the Excel workbook. Test missing values, alternate filters and refresh.
8. Save actual native dashboard to this directory as dashboard.pbip (Power BI) or dashboard.twbx (Tableau); export screenshots only after validating the visuals.

Limit: National estimates cannot produce state or wealth-group inequalities. Survey extensions remain pending.

Recommended layout: overview; trend and geographic comparison where supported; source and quality. No PBIX/PBIP/TWBX or published BI-service URL is claimed to exist in this release.
