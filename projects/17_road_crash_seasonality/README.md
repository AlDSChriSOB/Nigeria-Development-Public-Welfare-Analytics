# Road Crash Seasonality

Primary NBS/FRSC tables are now downloaded and analysed automatically.

```bash
python projects/17_road_crash_seasonality/python/run.py
```

Run from the repository root after installing requirements.txt. See [executed findings](reports/RESULTS.md), sql/primary_analysis.sql and outputs/primary_analysis.csv. All 22 quarter national totals reconcile to state counts. Native Power BI/Tableau authoring is deferred to the desktop session.

Quarterly totals do not reveal dangerous hours or weekdays. Event timestamps are required for finer timing.
