# Primary road-safety analysis progress

Projects 16 and 17 now execute primary NBS/FRSC state and quarter analyses. Project 18 executes contributing-factor distributions; the factor-by-severity question remains unresolved because the supplied aggregate tables do not link factors to individual outcomes.

22 quarters from Q4 2020 through Q1 2026, each with 37 state/FCT rows, were validated. Every count column reconciles to national totals; fatal/serious/minor counts reconcile to total crashes; injured and killed counts reconcile to casualties. Q1 2026 contributing-factor columns also reconcile to source totals.

## Verified observations
- Q1 2026: 2,720 reported crashes; +2.64% versus Q1 2025.
- Kaduna: 316 reported crashes, highest state count in Q1 2026.
- Counts are not per-journey risks. Factor mentions cannot establish factor-specific fatality rates.

## Desktop handoff
Use outputs/primary_analysis.csv for the project-specific dashboard, outputs/state_quarter.csv for state/quarter trends, and outputs/factor_mentions_q1_2026.csv for the factor case. Do not join factor mentions to deaths as if they were individual event records. Use period/state filters and explicit count units. Keep single-state Excel trend previews separate from national or state-ranking comparisons. Native BI authoring and validation is deferred to the user's laptop as agreed.

## Other sources
World Bank GHS microdata currently requires authenticated access. Afrobarometer CSV download returned HTTP 403 in this session. Those cases remain pending rather than being replaced with fabricated records.
