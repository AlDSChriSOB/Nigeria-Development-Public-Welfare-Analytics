# Verification and outstanding work

- 20 project directory structures and 20 three-sheet XLSX files verified.
- Six national WDI previews executed on real source data. SQL previous-observation changes cross-checked with independent pandas group calculations.
- Eleven primary-data cases return explicit AWAITING_PRIMARY_DATA states.
- Duplicate observation keys rejected in tests using duplicated actual source records.
- 20 notebook workflows executed sequentially through IPython; missing-data states are not completed analyses.
- Workbook formulas recalculated and inspected; error scans returned zero matches. Overview/Data/Methods sheets rendered during creation. These checks do not establish native Excel refresh behaviour.
- 20 Tableau TDS files parse as XML; Power Query, DAX and TDS assets have NOT been tested in native BI applications.
- No PBIX, native report dashboard, Tableau workbook, or BI service deployment is included or claimed.
- Native Power BI/Tableau software is unavailable in this execution environment. Original-source transformations, survey uncertainty and substantive case findings remain work to do.
- GitHub repository creation succeeded on the later refresh. See the remote Actions page for CI results; local execution alone does not establish remote CI success.

## Primary NBS update
Projects 16–17 execute verified state/quarter analyses; project 18 executes verified factor counts with the factor-by-severity linkage still unavailable. All 22×37 state-quarter count components and source totals reconcile. These three cases add primary-source outputs to the six national previews. See ROAD_PROGRESS.md. Native BI work is deferred to the user’s laptop.
